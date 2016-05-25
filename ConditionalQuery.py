import numpy as np
from cliqueSearch import cliqueSearch
from cliqueSearch import checkClique_one
from cliqueSearch import clique4
from cliqueSearch import searchClique_3
from cliqueSearch import searchClique_2
from networkStatistics import networkStatistics

#INPUT:
#	* ADJ_rank is the matrix of the ranking
#	* ADJ_sign is the matrix with the origina (signed) weights
#	* indices is a dictrionary that contains the indices of each category in the ADJ matrix
#	* queryInput is a dictionary that contains the indices of the query input divided by categories
#	* perc is the query percentile
#	* Each ogject in the neighborhoud subnetwork must be connected to at least minConnections object in the input
#	* minElemes is the minimum number of input object that must be in the final cliques
#OUTPUT:
#	* A dictionary containing sets of cliques. The dictionary is indexed by strings: 
#		* "NanoDrugDiseaseChemical": is the sets of cliques with 4 type of elements
#		* "NanoDrugDisease": is the sets of cliques containing only nano drug and disease
#		* "NanoDrugChemical"
#		* "NanoDiseaseChemical"
#		* "DrugDiseaseChemical"
#	* Each Set contains a list of tuples. There is a touple for each clique. 
#	* Each clique is represented by three tuples, the first one contains the index of the element in the clique, 
#	the second one the name of the element and the third one the list of the edges between the object
#	* Clique Edges are in the following order:
#		* "NanoDrugDiseaseChemical": nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem 
#		* "NanoDrugDisease": nano-drug nano-disease drug-disease
#		* "NanoDrugChemical" nano-drug nano-chemical drug-chemical
#		* "NanoDiseaseChemical" nano-disease nano-chemical disease-chemical
#		* "DrugDiseaseChemical" drug-disease drug-chemical disease-chemical

def ConditionalQuery(ADJ_rank,ADJ_sign,indices,queryInput,perc,minConnections,minElems,elemName):
	nClassQuery = sum([len(c)!=0 for c in queryInput.itervalues()])
	nNanoInput = len(queryInput['nano'])
	nDrugInput = len(queryInput['drug'])
	nChemicalInput = len(queryInput['chemical'])
	nDiseaseInput = len(queryInput['disease'])
	
	#You cant select a number of minimum connections bigger than the number of classes represented in the query
	#if(minConnections>nClassQuery):#Should I raise an exception here?
	#	print 'The number of minConnection must be less the the number of different classes represented in the input'
	#	return None

	#The number of minelems displayed in the final clique must be comprised between 1 and the number of classes represented in the query.
	#It can't be more than 4
	if(minElems>nClassQuery):#Should I raise an exception here?
		print 'The number of minElems must be less the the number of different classes represented in the input'
		return None

	#Removing all the connection that are higher that the percentile we want
	#ADJ[ADJ>=perc] = 0
	nElem = np.ceil(ADJ_rank.shape[0] * perc)
	ADJ_rank[ADJ_rank>nElem] = 0
	ADJ_rank[ADJ_rank!=0] = 1
	
	ADJ = ADJ_rank * ADJ_rank.T
	ADJ = ADJ * ADJ_sign
	
	#We are not interested in connections between two elements of the same class
	ADJ[np.ix_(indices['nano'],indices['nano'])]=0
	ADJ[np.ix_(indices['drug'],indices['drug'])]=0
	ADJ[np.ix_(indices['chemical'],indices['chemical'])]=0
	ADJ[np.ix_(indices['disease'],indices['disease'])]=0

	#Since rankings are not simmetric, we look for mutual neighborhood
#	NN_ADJ = ADJ * ADJ.T
	NN_ADJ = ADJ
	#We remove elements not connected to at least minConnections query element
	QI = [item for sublist in queryInput.values() for item in sublist]

	submatrix = NN_ADJ[QI,]
	submatrix[submatrix!=0]=1
	colSum = submatrix.sum(axis=0)

	neigIndex = colSum>=minConnections
	#We don't remove the query items from the subnetwork
	neigIndex[QI] = True

	if(neigIndex.sum()==0):
		print 'Non neighborhood, try to relax your thresholds'
		return None

	#NN_ADJ is the neighborhood submatrix that satisfy percentile and min connection thresholds
	neigIndexId = [i for i in range(len(neigIndex)) if neigIndex[i] == True]
	neigIndex =np.asarray(neigIndexId)

	#Object into NN_ADJ are in the order: NANO, DRUG, DISEASE, CHEMICAL
	NN_ADJ_red = NN_ADJ[np.ix_(neigIndex,neigIndex)]
	
	nEdges = np.count_nonzero(NN_ADJ_red)/2
	
	if(nEdges>1000000):
		print 'Too many edges in the network'
		return None
	
	nVertices = NN_ADJ_red.shape[0]
	
	#nanoOrigin contains the indices of the nanos in the original matrix
	nanoOrigin = list(set(neigIndex).intersection(set(indices['nano'])))
	nanoOrigin = np.sort(nanoOrigin).tolist() #I need to sort them, because in the submatrix are ordered increasingly
	#nano contains the indices of the nanos in the submatrix
	nano = range(len(nanoOrigin))

	drugOrigin = list(set(neigIndex).intersection(set(indices['drug'])))
	drugOrigin = np.sort(drugOrigin).tolist()
	drug = range(len(nano),len(nano)+len(drugOrigin))

	chemicalOrigin = list(set(neigIndex).intersection(set(indices['chemical'])))
	chemicalOrigin = np.sort(chemicalOrigin).tolist()
	chemical = range(len(nano)+len(drug), len(nano)+len(drug)+len(chemicalOrigin))

	diseaseOrigin = list(set(neigIndex).intersection(set(indices['disease'])))
	diseaseOrigin = np.sort(diseaseOrigin).tolist()
	disease = range(len(nano)+len(drug)+len(chemical),len(nano)+len(drug)+len(chemical)+len(diseaseOrigin))

	
	NS = networkStatistics(np.copy(NN_ADJ_red),ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
	
	if minElems == 4: #look for all quadruple of object in the input (one element for each class) and see if the form a clique
		print '4 minElems'
		CS4 = clique4(NN_ADJ,ADJ_sign,queryInput['nano'],queryInput['drug'],queryInput['chemical'],queryInput['disease'],elemName)
		Res4 = {'cliques':CS4,'nodes':NS['nodes'], 'edges':NS['edges']} 
		return Res4
		
	if minElems == 3:
		print '3 minElems'
		CS3 = searchClique_3(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
		Res3 = {'cliques':CS3,'nodes':NS['nodes'], 'edges':NS['edges']} 
		return Res3

	if minElems == 2:
		print 'minElems = 2'
		CS2 = searchClique_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
		Res2 = {'cliques':CS2,'nodes':NS['nodes'], 'edges':NS['edges']} 
		return Res2

	if minElems==1: #if minElems==1 I have to search for all the cliques
		print '1 minElems'
		CS = cliqueSearch(NN_ADJ_red,ADJ_sign,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
		Res = {'cliques':CS,'nodes':NS['nodes'], 'edges':NS['edges']} 
		return Res
	
	return None




