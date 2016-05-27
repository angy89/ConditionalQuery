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

	'''
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
	 '''				
	NodeEdges = {'nodes':nodes,'edges':edges}
	return(NodeEdges)
