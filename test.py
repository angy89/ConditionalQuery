#%load_ext autoreload
#%autoreload 2

import numpy as np
import itertools as it
import igraph
import time
from ConditionalQuery import ConditionalQuery

if __name__=='__main__':
	print 'Loading Adjacency Matrix'
	#colnames of ADJ are in the order nano-drug-chemical-disease
	#ADJ2 = np.loadtxt('../data/ADJ_perc2.txt',delimiter=',')

	ADJ_rank = np.loadtxt('../data/ADJ_rank.txt',delimiter=',')
	ADJ_sign = np.loadtxt('../data/ADJ_sign.txt',delimiter=',')
		
	print 'Loading indeces'
	nanoIdx = np.loadtxt('../data/nanoIndex.txt',dtype=np.int)
	drugIdx = np.loadtxt('../data/drugsIndex.txt',dtype=np.int)
	diseaseIdx = np.loadtxt('../data/diseaseIndex.txt',dtype=np.int)
	chemicalIdx = np.loadtxt('../data/chemIndex.txt',dtype=np.int)
	indices = {'nano':nanoIdx-1,'drug':drugIdx-1,'disease':diseaseIdx-1,'chemical':chemicalIdx-1}

	nanoBool = np.zeros(ADJ_rank.shape[0],dtype=np.bool)
	nanoBool[indices['nano']] = True
	
	drugBool = np.zeros(ADJ_rank.shape[0],dtype=np.bool)
	drugBool[indices['drug']] = True
	
	diseaseBool = np.zeros(ADJ_rank.shape[0],dtype=np.bool)
	diseaseBool[indices['disease']] = True
	
	chemicalBool = np.zeros(ADJ_rank.shape[0],dtype=np.bool)
	chemicalBool[indices['chemical']] = True

	indicesBool = {'nano':nanoBool,'drug':drugBool,'disease':diseaseBool,'chemical':chemicalBool}

	with open('../data/elemName.txt', 'r') as f:
		elemName = [s.strip() for s in f.readlines()]

	perc = 0.4
	queryInput = {'nano':[elemName.index("WCCo")],'drug':[elemName.index("levodopa")],'disease':[elemName.index("Parkinson Disease")],'chemical':[elemName.index("1-Methyl-4-phenyl-1,2,3,6-tetrahydropyridine")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 4
	minElems=3
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	end= time.clock()
	tempo = end-start
	
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['cliques']['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['cliques']['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['cliques']['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['cliques']['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['cliques']['DrugDiseaseChemical'])))


	perc = 0.01
	print 'Test 2: Testing cliqueSearch function'
	queryInput = {'nano':indices['nano'],'drug':indices['drug'],'disease':[],'chemical':[]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 2'
	
	CQ2 = CQ['cliques']
	nodes = CQ['nodes']
	edges = CQ['edges']
	
	ADJ_rank[np.ix_(list(CQ2['NanoDrugDisease'])[0][0],list(CQ2['NanoDrugDisease'])[0][0])]
	ADJ_rank[np.ix_(list(CQ2['NanoDrugDisease'])[1][0],list(CQ2['NanoDrugDisease'])[1][0])]
	ADJ_rank[np.ix_(list(CQ2['NanoDrugDisease'])[2][0],list(CQ2['NanoDrugDisease'])[2][0])]

	ADJ_sign[np.ix_(list(CQ2['NanoDrugDisease'])[0][0],list(CQ2['NanoDrugDisease'])[0][0])]

	nElem = np.ceil(ADJ_rank.shape[0] * perc)
	ADJ_rank[np.ix_(list(CQ2['NanoDrugDisease'])[0][0],list(CQ2['NanoDrugDisease'])[0][0])] < nElem

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 

		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ2['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ2['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ2['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ2['DrugDiseaseChemical'])))


	#	
	perc = 0.4
	nElem = np.ceil(ADJ_rank.shape[0] * perc)
	indici = [elemName.index('WCCo'),elemName.index('Parkinson Disease'),elemName.index('levodopa'),elemName.index('1-Methyl-4-phenyl-1,2,3,6-tetrahydropyridine')]
	ADJ_rank[np.ix_(indici,indici)]
	ADJ_rank[np.ix_(indici,indici)] <= nElem
	
	queryInput = {'nano':[elemName.index("WCCo")],'drug':[elemName.index("levodopa")],'disease':[elemName.index("Parkinson Disease")],'chemical':[]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 3
	minElems=3
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	CQ = CQ['cliques']




	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)	
	print 'End!'
	
	
	ADJ_rank[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])]
	ADJ_sign[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])]



	#	
	perc = 0.4
	indici = [elemName.index('TiO2'),elemName.index('Bronchitis'),elemName.index('cefepime'),elemName.index('Air Pollutants')]
	ADJ_rank[np.ix_(indici,indici)]
	
	queryInput = {'nano':[elemName.index("TiO2")],'drug':[elemName.index("cefepime")],'disease':[elemName.index("Bronchitis")],'chemical':[elemName.index("Air Pollutants")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 4
	minElems=4
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	CQ = CQ['cliques']

	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)	
	print 'End!'
	
	
	ADJ_rank[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])]
	ADJ_sign[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])]

	
	
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))
	
	
	
	#
	perc = 0.4
	queryInput = {'nano':[elemName.index("TiO2")],'drug':[elemName.index("cefepime")],'disease':[elemName.index("Bronchitis")],'chemical':[elemName.index("Air Pollutants")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 4
	minElems=2
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	CQ = CQ['cliques']
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	
	print 'End!'

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))

	nElem = np.ceil(ADJ_rank.shape[0] * perc)

	ADJ_rank[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])] < nElem 
	ADJ_sign[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])]


	#
	perc = 0.3
	queryInput = {'nano':[elemName.index("ZnO4")],'drug':[elemName.index("prochlorperazine")],'disease':[elemName.index("Dementia")],'chemical':[elemName.index("Zinc")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 4
	minElems=2
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	CQ = CQ['cliques']
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	
	print 'End!'

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))
	
	nElem = np.ceil(ADJ_rank.shape[0] * perc)

	ADJ_rank[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])] < nElem 
	ADJ_sign[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])]

	
	#
	perc = 0.3
	queryInput = {'nano':[elemName.index("ZnO4")],'drug':[elemName.index("prochlorperazine")],'disease':[elemName.index("Dementia")],'chemical':[elemName.index("Zinc")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 4
	minElems=4
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	CQ = CQ['cliques']
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	
	print 'End!'

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))

	#
	perc = 0.1
	queryInput = {'nano':[elemName.index("AgNP")],'drug':[elemName.index("diflorasone")],'disease':[elemName.index("Dermatitis, Atopic")],'chemical':[elemName.index("Methoxychlor")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 2
	minElems=1
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	CQ = CQ['cliques']
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	
	print 'End!'

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))
	
	nElem = np.ceil(ADJ_rank.shape[0] * perc)

	ADJ_rank[np.ix_(list(CQ['NanoDrugDiseaseChemical'])[0][0],list(CQ['NanoDrugDiseaseChemical'])[0][0])] < nElem 
	ADJ_rank[np.ix_(list(CQ['NanoDrugDisease'])[0][0],list(CQ['NanoDrugDisease'])[0][0])] < nElem 


	perc = 0.1
	print 'Test 2: Testing cliqueSearch function'
	queryInput = {'nano':[0,9,20],'drug':[325,46],'disease':[3309],'chemical':[2087,2561]}
	minConnections = 4
	minElems=1
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	#CQ = CQ['cliques']
	print 'End Test 2'

	print 'Test 1: Testing clique4 function'
	queryInput = {'nano':[0,9,20],'drug':[325,46],'disease':[3309],'chemical':[2087,2561]}
	minConnections = 4
	minElems=4
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	CQ = CQ['cliques']
	print 'End Test 1'



	#
	perc = 0.3
	queryInput = {'nano':[0,9,20],'drug':[325,46],'disease':[3309],'chemical':[2087,2561]}
	minConnections = 4
	minElems=1
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	CQ = CQ['cliques']
	print 'End!'

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))



	perc = 0.4
	queryInput = {'nano':[elemName.index("AuNP")],'drug':[elemName.index("quinidine")],'disease':[elemName.index("Amyotrophic Lateral Sclerosis")],'chemical':[elemName.index("Pyrethrins")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 3
	minElems=3
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	CQ = CQ['cliques']
	print 'End!'

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))

	#
	perc = 0.4
	queryInput = {'nano':[elemName.index("TiO2")],'drug':[elemName.index("cefepime")],'disease':[elemName.index("Bronchitis")],'chemical':[elemName.index("Air Pollutants")]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 3
	minElems=3
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	
	print 'End!'
	CQ = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))
		
		
	print 'Test 9: Testing searchClique_3 function (nano-drug-disease)'
	queryInput = {'nano':[20],'drug':[325],'disease':[3309],'chemical':[]}
	minConnections = 3
	minElems=3
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 9'
	
	print 'Test 10: Testing searchClique_3 function (nano-drug-chemical)'
	queryInput = {'nano':[20],'drug':[325],'disease':[],'chemical':[2087]}
	minConnections = 3
	minElems=3
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 10'
	
	print 'Test 11: Testing searchClique_3 function (nano-disease-chemical)'
	queryInput = {'nano':[20],'drug':[],'disease':[3309],'chemical':[2087]}
	minConnections = 3
	minElems=3
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 11'
	
	print 'Test 12: Testing searchClique_3 function (drug-disease-chemical)'
	queryInput = {'nano':[],'drug':[325],'disease':[3309],'chemical':[2087]}
	minConnections = 3
	minElems=3
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 12'
	

	
	perc = 0.05
	print 'Test 2: Testing cliqueSearch function'
	queryInput = {'nano':[],'drug':[],'disease':indices['disease'],'chemical':indices['chemical']}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 2'
	
	CQ2 = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 

		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ2['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ2['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ2['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ2['DrugDiseaseChemical'])))

	
	
	perc = 0.05
	print 'Test 2: Testing cliqueSearch function'
	queryInput = {'nano':[],'drug':indices['drug'],'disease':[],'chemical':indices['chemical']}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 2'
	
	CQ2 = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 

		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ2['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ2['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ2['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ2['DrugDiseaseChemical'])))

	
	
	perc = 0.05
	print 'Test 2: Testing cliqueSearch function'
	queryInput = {'nano':[],'drug':indices['drug'],'disease':indices['disease'],'chemical':[]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 2'
	
	CQ2 = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 

		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ2['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ2['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ2['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ2['DrugDiseaseChemical'])))

	
	
	perc = 0.05
	print 'Test 2: Testing cliqueSearch function'
	queryInput = {'nano':indices['nano'],'drug':[],'disease':[],'chemical':indices['chemical']}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 2'
	
	CQ2 = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 

		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ2['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ2['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ2['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ2['DrugDiseaseChemical'])))

	
	
	perc = 0.05
	print 'Test 2: Testing cliqueSearch function'
	queryInput = {'nano':indices['nano'],'drug':[],'disease':indices['disease'],'chemical':[]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 2'
	
	CQ2 = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical'])))
	else:
		print 'Vertices in the network: {}'.format(len(list(CQ['nodes']))) 
		print 'Edges in the network {}'.format(len(list(CQ['edges']))) 

		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ2['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ2['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ2['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ2['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ2['DrugDiseaseChemical'])))
	
	perc = 0.4
	print 'Test 3: Testing searchClique_2 function (drug-disease)'
	queryInput = {'nano':[],'drug':[325],'disease':[3309],'chemical':[]}
	minConnections = 2
	minElems=2
	
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 3 (drug-disease)'
	
	print 'Test 4: Testing searchClique_2 function (nano-drug)'
	queryInput = {'nano':[20],'drug':[325],'disease':[],'chemical':[]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 4 (nano-drug)'
	
	print 'Test 5: Testing searchClique_2 function (nano-disease)'
	queryInput = {'nano':[20],'drug':[],'disease':[3309],'chemical':[]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 5 (nano-disease)'
	
	print 'Test 6: Testing searchClique_2 function (nano-chemical)'
	queryInput = {'nano':[20],'drug':[],'disease':[],'chemical':[2087]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 6 (nano-chemical)'
	
	print 'Test 7: Testing searchClique_2 function (drug-chemical)'
	queryInput = {'nano':[],'drug':[325],'disease':[],'chemical':[2087]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 7 (drug-chemical)'
	
	print 'Test 8: Testing searchClique_2 function (disease-chemical)' #PROBLEMS
	queryInput = {'nano':[],'drug':[],'disease':[3309],'chemical':[2087]}
	minConnections = 2
	minElems=2
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	print 'End Test 8 (disease-chemical)'
	
	perc = 0.3
	queryInput = {'nano':[elemName.index("AgNP")],'drug':[],'disease':[elemName.index("Dermatitis, Atopic")],'chemical':[]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 2
	minElems=2
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	CQ = CQ['cliques']
	print 'End!'

	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))
		

	#
	perc = 0.4
	queryInput = {'nano':[],'drug':[elemName.index("levodopa")],'disease':[elemName.index("Parkinson Disease")],'chemical':[]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 2
	minElems=2
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	
	print 'End!'
	CQ = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))
		
	#
	perc = 0.48
	queryInput = {'nano':[elemName.index("MWCNT")],'drug':[],'disease':[elemName.index("Pulmonary Disease, Chronic Obstructive")],'chemical':[]}
	QI = [item for sublist in queryInput.values() for item in sublist]
	ADJ_rank[np.ix_(QI,QI)]
	minConnections = 2
	minElems=2
	print 'Run Conditional Query'
	start= time.clock()
	CQ = ConditionalQuery(np.copy(ADJ_rank),ADJ_sign,indices,indicesBool,queryInput,perc,minConnections,minElems,elemName)
	end= time.clock()
	tempo = end-start
	print 'Time lapsed: {}'.format(tempo)
	
	print 'End!'
	CQ = CQ['cliques']
	if minElems==4:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical'])))
	else:
		print 'Nano - Drug - Disease - Chemical: {}'.format(len(list(CQ['NanoDrugDiseaseChemical']))) 
		print 'Nano - Drug - Disease: {}'.format(len(list(CQ['NanoDrugDisease'])))
		print 'Nano - Drug  - Chemical: {}'.format(len(list(CQ['NanoDrugChemical'])))
		print 'Nano  - Disease - Chemical: {}'.format(len(list(CQ['NanoDiseaseChemical'])))
		print 'Drug - Disease - Chemical: {}'.format(len(list(CQ['DrugDiseaseChemical'])))






