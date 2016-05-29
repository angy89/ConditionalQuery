import random
import numpy as np
from collections import namedtuple
Edge = namedtuple('Edge',['id','source','type','target','color','weight'])
Node = namedtuple('Node',['id','label','size','color','type','x','y','degree'])

def networkStatistics(CS,ADJ_sign,indicesBool,elemName):

	NDrDiC = list(CS['NanoDrugDiseaseChemical'])
	NDrDi = list(CS['NanoDrugDisease'])
	NDrC = list(CS['NanoDrugChemical'])
	NDiC = list(CS['NanoDiseaseChemical'])
	DrDiC = list(CS['DrugDiseaseChemical'])

	eIdx = 1
	edges = set()
	nodesID = set()

	for i in range(len(NDrDiC)):
		for j in range(4):
			nodesID.add(NDrDiC[i][0][j])

	for i in range(len(NDrDi)):
		for j in range(3):
			nodesID.add(NDrDi[i][0][j])

	for i in range(len(NDrC)):
		for j in range(3):
			nodesID.add(NDrC[i][0][j])

	for i in range(len(NDiC)):
		for j in range(3):
			nodesID.add(NDiC[i][0][j])

	for i in range(len(DrDiC)):
		for j in range(3):
			nodesID.add(DrDiC[i][0][j])

	nodesID = list(nodesID)
	Net = np.zeros_like(ADJ_sign)

	for i in range(len(NDrDiC)):
		res = NDrDiC_Net(NDrDiC[i][0][0],NDrDiC[i][0][1],NDrDiC[i][0][2],NDrDiC[i][0][3],ADJ_sign,eIdx,Net)
		Net = res['Net']
		eIdx = res['eIdx']
		edges.update(res['edges'])

	for i in range(len(NDrDi)):
		res = NDrDi_Net(NDrDi[i][0][0],NDrDi[i][0][1],NDrDi[i][0][2],ADJ_sign,eIdx,Net)
		Net = res['Net']
		eIdx = res['eIdx']
		edges.update(res['edges'])

	for i in range(len(NDrC)):
		res = NDrC_Net(NDrC[i][0][0],NDrC[i][0][1],NDrC[i][0][2],ADJ_sign,eIdx,Net)
		Net = res['Net']
		eIdx = res['eIdx']
		edges.update(res['edges'])

	for i in range(len(NDiC)):
		res = NDiC_Net(NDiC[i][0][0],NDiC[i][0][1],NDiC[i][0][2],ADJ_sign,eIdx,Net)
		Net = res['Net']
		eIdx = res['eIdx']
		edges.update(res['edges'])

	for i in range(len(DrDiC)):
		res = DrDiC_Net(DrDiC[i][0][0],DrDiC[i][0][1],DrDiC[i][0][2],ADJ_sign,eIdx,Net)
		Net = res['Net']
		eIdx = res['eIdx']
		edges.update(res['edges'])

	nodes = set()
	for i in range(len(nodesID)):
		nodes.update(generateNode(nodesID[i],indicesBool,Net,elemName))

	return {'nodes':nodes,'edges':edges}

def generateNode(nodeId,indicesBool,Net,elemName):
	node_color = {}
	node_color['nano'] = '#ff0000'
	node_color['drug'] = '#0000ff'
	node_color['chemical'] = '#00ff00'
	node_color['disease'] = '#ff00ff'
	
	#nodePos = nodesID.index(nodeID)
	nodeDegree = np.sum(Net[nodeId,:]!=0)
	node = []
	
	if indicesBool['nano'][nodeId]:
		node.append(Node(id= nodeId, label= elemName[nodeId], size= 1, color= node_color['nano'],type='nano',x= random.randint(0, 1000), y= random.randint(0, 1000),degree=nodeDegree))

	if indicesBool['drug'][nodeId]:
		node.append(Node(id= nodeId, label= elemName[nodeId], size= 1, color= node_color['drug'],type='drug',x= random.randint(0, 1000), y= random.randint(0, 1000),degree=nodeDegree))

	if indicesBool['disease'][nodeId]:
		node.append(Node(id= nodeId, label= elemName[nodeId], size= 1, color= node_color['disease'],type='disease',x= random.randint(0, 1000), y= random.randint(0, 1000),degree=nodeDegree))

	if indicesBool['chemical'][nodeId]:
		node.append(Node(id= nodeId, label= elemName[nodeId], size= 1, color= node_color['chemical'],type='chemical',x= random.randint(0, 1000), y= random.randint(0, 1000),degree=nodeDegree))

	return node

def NDrDiC_Net(nanoIndex,drugIndex,diseaseIndex,chemicalIndex,ADJ_sign,eIdx,Net):

	pEdgeCol = '#ff9999'
	nEdgeCol = '#99ff99'

	edges = []

	Net[nanoIndex,drugIndex]  = ADJ_sign[nanoIndex,drugIndex]
	Net[drugIndex,nanoIndex] = ADJ_sign[nanoIndex,drugIndex]
	
	Net[nanoIndex,diseaseIndex] = ADJ_sign[nanoIndex,diseaseIndex]
	Net[diseaseIndex,nanoIndex] = ADJ_sign[nanoIndex,diseaseIndex]

	Net[nanoIndex,chemicalIndex] = ADJ_sign[nanoIndex,chemicalIndex]
	Net[chemicalIndex,nanoIndex] = ADJ_sign[nanoIndex,chemicalIndex]

	Net[drugIndex,diseaseIndex] = ADJ_sign[drugIndex,diseaseIndex]
	Net[diseaseIndex,drugIndex] = ADJ_sign[drugIndex,diseaseIndex]

	Net[drugIndex,chemicalIndex] = ADJ_sign[drugIndex,chemicalIndex]
	Net[chemicalIndex,drugIndex] = ADJ_sign[drugIndex,chemicalIndex]

	Net[diseaseIndex,chemicalIndex] = ADJ_sign[diseaseIndex,chemicalIndex]
	Net[chemicalIndex,diseaseIndex] = ADJ_sign[diseaseIndex,chemicalIndex]

	
	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= drugIndex, color= pEdgeCol if ADJ_sign[nanoIndex,drugIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,drugIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= diseaseIndex, color= pEdgeCol if ADJ_sign[nanoIndex,diseaseIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,diseaseIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[nanoIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,chemicalIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= drugIndex, type= 'curvedArrow', target= diseaseIndex, color= pEdgeCol if ADJ_sign[drugIndex,diseaseIndex]>0 else nEdgeCol,weight=ADJ_sign[drugIndex,diseaseIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= drugIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[drugIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[drugIndex,chemicalIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= diseaseIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[diseaseIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[diseaseIndex,chemicalIndex]))
	eIdx +=1
	
	#return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
	return {'edges':edges, 'eIdx':eIdx,'Net': Net}


def NDrDi_Net(nanoIndex,drugIndex,diseaseIndex,ADJ_sign,eIdx,Net):
	pEdgeCol = '#ff9999'
	nEdgeCol = '#99ff99'
	
	edges = []

	Net[nanoIndex,drugIndex]  = ADJ_sign[nanoIndex,drugIndex]
	Net[drugIndex,nanoIndex] = ADJ_sign[nanoIndex,drugIndex]
	
	Net[nanoIndex,diseaseIndex] = ADJ_sign[nanoIndex,diseaseIndex]
	Net[diseaseIndex,nanoIndex] = ADJ_sign[nanoIndex,diseaseIndex]

	Net[drugIndex,diseaseIndex] = ADJ_sign[drugIndex,diseaseIndex]
	Net[diseaseIndex,drugIndex] = ADJ_sign[drugIndex,diseaseIndex]

	
	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= drugIndex, color= pEdgeCol if ADJ_sign[nanoIndex,drugIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,drugIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= diseaseIndex, color= pEdgeCol if ADJ_sign[nanoIndex,diseaseIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,diseaseIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= drugIndex, type= 'curvedArrow', target= diseaseIndex, color= pEdgeCol if ADJ_sign[drugIndex,diseaseIndex]>0 else nEdgeCol,weight=ADJ_sign[drugIndex,diseaseIndex]))
	eIdx +=1	
	
	#return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
	return {'edges':edges, 'eIdx':eIdx,'Net': Net}

def NDrC_Net(nanoIndex,drugIndex,chemicalIndex,ADJ_sign,eIdx,Net):

	pEdgeCol = '#ff9999'
	nEdgeCol = '#99ff99'

	edges = []


	Net[nanoIndex,drugIndex]  = ADJ_sign[nanoIndex,drugIndex]
	Net[drugIndex,nanoIndex] = ADJ_sign[nanoIndex,drugIndex]

	Net[nanoIndex,chemicalIndex] = ADJ_sign[nanoIndex,chemicalIndex]
	Net[chemicalIndex,nanoIndex] = ADJ_sign[nanoIndex,chemicalIndex]

	Net[drugIndex,chemicalIndex] = ADJ_sign[drugIndex,chemicalIndex]
	Net[chemicalIndex,drugIndex] = ADJ_sign[drugIndex,chemicalIndex]

	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= drugIndex, color= pEdgeCol if ADJ_sign[nanoIndex,drugIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,drugIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[nanoIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,chemicalIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= drugIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[drugIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[drugIndex,chemicalIndex]))
	eIdx +=1
	
	#return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}	
	return {'edges':edges, 'eIdx':eIdx,'Net': Net}

def NDiC_Net(nanoIndex,diseaseIndex,chemicalIndex,ADJ_sign,eIdx,Net):

	pEdgeCol = '#ff9999'
	nEdgeCol = '#99ff99'

	edges = []

	Net[nanoIndex,diseaseIndex] = ADJ_sign[nanoIndex,diseaseIndex]
	Net[diseaseIndex,nanoIndex] = ADJ_sign[nanoIndex,diseaseIndex]

	Net[nanoIndex,chemicalIndex] = ADJ_sign[nanoIndex,chemicalIndex]
	Net[chemicalIndex,nanoIndex] = ADJ_sign[nanoIndex,chemicalIndex]

	Net[diseaseIndex,chemicalIndex] = ADJ_sign[diseaseIndex,chemicalIndex]
	Net[chemicalIndex,diseaseIndex] = ADJ_sign[diseaseIndex,chemicalIndex]

	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= diseaseIndex, color= pEdgeCol if ADJ_sign[nanoIndex,diseaseIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,diseaseIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= nanoIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[nanoIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[nanoIndex,chemicalIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= diseaseIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[diseaseIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[diseaseIndex,chemicalIndex]))
	eIdx +=1
	
	#return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
	return {'edges':edges, 'eIdx':eIdx,'Net': Net}

def DrDiC_Net(drugIndex,diseaseIndex,chemicalIndex,ADJ_sign,eIdx,Net):
	pEdgeCol = '#ff9999'
	nEdgeCol = '#99ff99'

	edges = []

	Net[drugIndex,diseaseIndex] = ADJ_sign[drugIndex,diseaseIndex]
	Net[diseaseIndex,drugIndex] = ADJ_sign[drugIndex,diseaseIndex]

	Net[drugIndex,chemicalIndex] = ADJ_sign[drugIndex,chemicalIndex]
	Net[chemicalIndex,drugIndex] = ADJ_sign[drugIndex,chemicalIndex]

	Net[diseaseIndex,chemicalIndex] = ADJ_sign[diseaseIndex,chemicalIndex]
	Net[chemicalIndex,diseaseIndex] = ADJ_sign[diseaseIndex,chemicalIndex]

	edges.append(Edge(id=eIdx, source= drugIndex, type= 'curvedArrow', target= diseaseIndex, color= pEdgeCol if ADJ_sign[drugIndex,diseaseIndex]>0 else nEdgeCol,weight=ADJ_sign[drugIndex,diseaseIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= drugIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[drugIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[drugIndex,chemicalIndex]))
	eIdx +=1
	
	edges.append(Edge(id=eIdx, source= diseaseIndex, type= 'curvedArrow', target= chemicalIndex, color= pEdgeCol if ADJ_sign[diseaseIndex,chemicalIndex]>0 else nEdgeCol,weight=ADJ_sign[diseaseIndex,chemicalIndex]))
	eIdx +=1
	
	#return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
	return {'edges':edges, 'eIdx':eIdx,'Net': Net}


'''
import numpy as np

def networkStatistics(NN_ADJ,ADJ_sign,neigIndex,indices,nano,drug,chemical,disease,queryInput,elemName):
	nodes = []
	for nn in range(len(indices['nano'])):
		if(nano[indices['nano'][nn]]):
			nodes.append({'id':indices['nano'][nn],'label':elemName[indices['nano'][nn]],'type':'nano'})
		
	for dd in range(len(indices['drug'])):
		if(drug[indices['drug'][dd]]):
			nodes.append({'id':indices['drug'][dd],'label':elemName[indices['drug'][dd]],'type':'drug'})

	for di in range(len(indices['disease'])):
		if(disease[indices['disease'][di]]):
			nodes.append({'id':indices['disease'][di],'label':elemName[indices['disease'][di]],'type':'disease'})
			
	for cc in range(len(indices['chemical'])):
		if(chemical[indices['chemical'][cc]]):
			nodes.append({'id':indices['chemical'][cc],'label':elemName[indices['chemical'][cc]],'type':'chemical'})
	
	edges = []

	nnz = np.tril(NN_ADJ).nonzero()
	
	for row,col in zip(nnz[0],nnz[1]): 
		source = target = None
		if nano[row]:
			source = row
		elif drug[row]:
			source = row
		elif disease[row]:
			source = row
		elif chemical[row]:
			source = row
	
		if nano[col]:
			target = col
		elif drug[col]:
			target = col
		elif disease[col]:
			target = col
		elif chemical[col]:
			target = col
	
		if(source is not None and target is not None):
			d={'source':source,'target':target,'weight':ADJ_sign[source,target]}
			#print d
			edges.append(d)

	
	for nn in range(len(nano)):
		nanoIndex = nanoOrigin[nn]
		for dd in range(len(drug)):
			drugIndex = drugOrigin[dd]
			nano_drug = NN_ADJ_red[nano[nn],drug[dd]]!=0
			if(nano_drug):
				edges.append({'source':nanoIndex,'target':drugIndex,'weight':ADJ_sign[nanoIndex,drugIndex]})
			for di in range(len(diseasePos)):
				diseaseIndex = diseaseOrigin[di]
				nano_disease = NN_ADJ_red[nano[nn],disease[di]]!=0
				
				if(nano_disease):
					edges.append({'source':nanoIndex,'target':diseaseIndex,'weight':ADJ_sign[nanoIndex,diseaseIndex]})
				
				drug_disease = NN_ADJ_red[drug[dd],disease[di]]!=0
				if(drug_disease):
					edges.append({'source':drugIndex,'target':diseaseIndex,'weight':ADJ_sign[drugIndex,diseaseIndex]})
				for cc in range(len(chemical)):
					chemicalIndex = chemicalOrigin[cc]	
					
					nano_chemical = NN_ADJ_red[nano[nn],chemical[cc]]!=0
					if(nano_chemical):
						edges.append({'source':nanoIndex,'target':chemicalIndex,'weight':ADJ_sign[nanoIndex,chemicalIndex]})
					
					drug_chemical = NN_ADJ_red[drug[dd],chemical[cc]]!=0
					if(drug_chemical):
						edges.append({'source':drugIndex,'target':chemicalIndex,'weight':ADJ_sign[drugIndex,chemicalIndex]})
					
					disease_chemical = NN_ADJ_red[disease[di],chemical[cc]]!=0
					if(disease_chemical):
						edges.append({'source':diseaseIndex,'target':chemicalIndex,'weight':ADJ_sign[diseaseIndex,chemicalIndex]})
	 			
	NodeEdges = {'nodes':nodes,'edges':edges}
	return(NodeEdges)
'''
