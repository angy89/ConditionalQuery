import sys
import numpy as np
from cliqueSearch import cliqueSearch
from cliqueSearch import checkClique_one
from cliqueSearch import clique4
from cliqueSearch import searchClique_3
from cliqueSearch import searchClique_2
from networkStatistics import networkStatistics


# INPUT:
#	* ADJ_rank is the matrix of the ranking
#	* ADJ_sign is the matrix with the origina (signed) weights
#	* indices is a dictrionary that contains the indices of each category in the ADJ matrix
#	* queryInput is a dictionary that contains the indices of the query input divided by categories
#	* perc is the query percentile
#	* Each ogject in the neighborhoud subnetwork must be connected to at least minConnections object in the input
#	* minElemes is the minimum number of input object that must be in the final cliques
# OUTPUT:
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

def ConditionalQuery(ADJ_rank, ADJ_sign,ADJ_known, indices, indicesBool, queryInput, perc, minConnections, minElems, elemName):
    nClassQuery = sum([len(c) != 0 for c in queryInput.itervalues()])
    nNanoInput = len(queryInput['nano'])
    nDrugInput = len(queryInput['drug'])
    nChemicalInput = len(queryInput['chemical'])
    nDiseaseInput = len(queryInput['disease'])

    # The number of minelems displayed in the final clique must be comprised between 1 and the number of classes represented in the query.
    # It can't be more than 4
    if (minElems > nClassQuery):  # Should I raise an exception here?
        return {
            'error': 'Minimum elements in cliques must be lower or equal to the number of different classes represented in the input'
        }

    # Removing all the connection that are higher that the percentile we want
    # ADJ[ADJ>=perc] = 0
    nElem = np.ceil(ADJ_rank.shape[0] * perc)
    ADJ_rank[ADJ_rank > nElem] = 0
    ADJ_rank[ADJ_rank != 0] = 1
    ADJ = ADJ_rank * ADJ_rank.T
    NN_ADJ = ADJ * ADJ_sign

    # We are not interested in connections between two elements of the same class
    NN_ADJ[np.ix_(indices['nano'], indices['nano'])] = 0
    NN_ADJ[np.ix_(indices['drug'], indices['drug'])] = 0
    NN_ADJ[np.ix_(indices['chemical'], indices['chemical'])] = 0
    NN_ADJ[np.ix_(indices['disease'], indices['disease'])] = 0

    QI = [item for sublist in queryInput.values() for item in sublist]

    submatrix = NN_ADJ[QI,]
    submatrix[submatrix != 0] = 1
    colSum = submatrix.sum(axis=0)

    neigIndex = colSum >= minConnections
    neigIndex[QI] = True  # We don't remove the query items from the subnetwork

    nano = neigIndex & indicesBool['nano']
    drug = neigIndex & indicesBool['drug']
    disease = neigIndex & indicesBool['disease']
    chemical = neigIndex & indicesBool['chemical']

    # nEdges = len(np.tril(NN_ADJ[np.ix_(neigIndex,neigIndex)]).nonzero()[0])
    nEdges = np.count_nonzero(NN_ADJ[np.ix_(neigIndex, neigIndex)]) / 2
    nVertices = np.sum(neigIndex)

    if (nEdges > 1000000):
        return {
            'error': 'There are too many edges in the sub-network, please decrease the interaction threshold or remove some nodes'
        }
    #sys.stderr.write("edges in subnet: " + str(nEdges))

    if minElems == 4:  # look for all quadruple of object in the input (one element for each class) and see if the form a clique
        CS4 = clique4(NN_ADJ, ADJ_sign, ADJ_known,queryInput, elemName)
        NS = networkStatistics(CS4, ADJ_sign, ADJ_known,indicesBool, elemName)
        Res4 = {'cliques': CS4, 'nodes': NS['nodes'], 'edges': NS['edges']}
        return Res4

    if minElems == 3:
        CS3 = searchClique_3(NN_ADJ, ADJ_sign, ADJ_known,nNanoInput, nDrugInput, nChemicalInput, nDiseaseInput, nano, drug,
                             chemical, disease, queryInput, elemName)
        NS = networkStatistics(CS3, ADJ_sign, ADJ_known,indicesBool, elemName)
        Res3 = {'cliques': CS3, 'nodes': NS['nodes'], 'edges': NS['edges']}
        return Res3

    if minElems == 2:
        CS2 = searchClique_2(NN_ADJ, ADJ_sign,ADJ_known, nNanoInput, nDrugInput, nChemicalInput, nDiseaseInput, nano, drug,
                             chemical, disease, queryInput, elemName)
        NS = networkStatistics(CS2, ADJ_sign, ADJ_known,indicesBool, elemName)
        Res2 = {'cliques': CS2, 'nodes': NS['nodes'], 'edges': NS['edges']}
        return Res2

    if minElems == 1:  # if minElems==1 I have to search for all the cliques
        CS = cliqueSearch(NN_ADJ, ADJ_sign, ADJ_known,nano, drug, disease, chemical, queryInput, elemName)
        NS = networkStatistics(CS, ADJ_sign, ADJ_known, indicesBool, elemName)
        Res = {'cliques': CS, 'nodes': NS['nodes'], 'edges': NS['edges']}
        return Res

    return {'error': 'Input processing failed'}
