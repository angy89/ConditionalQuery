import numpy as np

def networkStatistics(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	nodes = []
	for nn in range(len(nano)):
		nanoIndex = nanoIndex = nanoOrigin[nn]
		nodes.append({'id':nanoIndex,'label':elemName[nanoIndex],'type':'nano'})
		
	for dd in range(len(drug)):
		drugIndex = drugOrigin[dd]
		nodes.append({'id':drugIndex,'label':elemName[drugIndex],'type':'drug'})

	for di in range(len(disease)):
		diseaseIndex = diseaseOrigin[di]
		nodes.append({'id':diseaseIndex,'label':elemName[diseaseIndex],'type':'disease'})

	for cc in range(len(chemical)):
		chemicalIndex = chemicalOrigin[cc]	
		nodes.append({'id':chemicalIndex,'label':elemName[chemicalIndex],'type':'chemical'})
	
	edges = []
	
	nnz = np.tril(NN_ADJ_red).nonzero()
	
	for row,col in zip(nnz[0],nnz[1]): 
		if row in nano:
			source = nanoOrigin[nano.index(row)]
		elif row in drug:
			source = drugOrigin[drug.index(row)]
		elif row in disease:
			source = diseaseOrigin[disease.index(row)]
		else:
			source = chemicalOrigin[chemical.index(row)]		
	
		if col in nano:
			target = nanoOrigin[nano.index(col)]
		elif col in drug:
			target = drugOrigin[drug.index(col)]
		elif col in disease:
			target = diseaseOrigin[disease.index(col)]
		else:
			target = chemicalOrigin[chemical.index(col)]		
	
		edges.append({'source':source,'target':target,'weight':ADJ_sign[source,target]})
	
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
