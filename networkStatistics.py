def networkStatistics(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	nanoPos = [] #nanoPos contains the indices in the submatrix of the original nano in the query
	for i in range(len(queryInput['nano'])):
		nanoPos.append(nano[nanoOrigin.index(queryInput['nano'][i])])
	drugPos = []
	for i in range(len(queryInput['drug'])):
		drugPos.append(drug[drugOrigin.index(queryInput['drug'][i])])
	diseasePos = []
	for i in range(len(queryInput['disease'])):
		diseasePos.append(disease[diseaseOrigin.index(queryInput['disease'][i])])
	chemicalPos = []
	for i in range(len(queryInput['chemical'])):
		chemicalPos.append(chemical[chemicalOrigin.index(queryInput['chemical'][i])])
	
	
	nodes = []
	for nn in range(len(nanoPos)):
		nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
		nodes.append({'id':nanoIndex,'label':elemName[nanoIndex],'type':'nano'})
		
	for dd in range(len(drugPos)):
		drugIndex = drugOrigin[drug.index(drugPos[dd])]
		nodes.append({'id':drugIndex,'label':elemName[drugIndex],'type':'drug'})

	for di in range(len(diseasePos)):
		diseaseIndex = diseaseOrigin[disease.index(diseasePos[di])]
		nodes.append({'id':diseaseIndex,'label':elemName[diseaseIndex],'type':'disease'})

	for cc in range(len(chemicalPos)):
		chemicalIndex = chemicalOrigin[chemical.index(chemicalPos[cc])]	
		nodes.append({'id':chemicalIndex,'label':elemName[chemicalIndex],'type':'chemical'})
	
	edges = []
	
	for nn in range(len(nanoPos)):
		nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
		for dd in range(len(drugPos)):
			drugIndex = drugOrigin[drug.index(drugPos[dd])]
			nano_drug = NN_ADJ_red[nanoPos[nn],drugPos[dd]]!=0
			if(nano_drug):
				edges.append({'source':nanoIndex,'target':drugIndex,'weight':ADJ_sign[nanoIndex,drugIndex]})
			for di in range(len(diseasePos)):
				diseaseIndex = diseaseOrigin[disease.index(diseasePos[di])]
				nano_disease = NN_ADJ_red[nanoPos[nn],diseasePos[di]]!=0
				
				if(nano_disease):
					edges.append({'source':nanoIndex,'target':diseaseIndex,'weight':ADJ_sign[nanoIndex,drugIndex]})
				
				drug_disease = NN_ADJ_red[drugPos[dd],diseasePos[di]]!=0
				if(drug_disease):
					edges.append({'source':drugIndex,'target':diseaseIndex,'weight':ADJ_sign[drugIndex,diseaseIndex]})
				for cc in range(len(chemicalPos)):
					chemicalIndex = chemicalOrigin[chemical.index(chemicalPos[cc])]	
					
					nano_chemical = NN_ADJ_red[nanoPos[nn],chemicalPos[cc]]!=0
					if(nano_chemical):
						edges.append({'source':nanoIndex,'target':chemicalIndex,'weight':ADJ_sign[nanoIndex,chemicalIndex]})
					
					drug_chemical = NN_ADJ_red[drugPos[dd],chemicalPos[cc]]!=0
					if(drug_chemical):
						edges.append({'source':drugIndex,'target':chemicalIndex,'weight':ADJ_sign[drugIndex,chemicalIndex]})
					
					disease_chemical = NN_ADJ_red[diseasePos[di],chemicalPos[cc]]!=0
					if(disease_chemical):
						edges.append({'source':diseaseIndex,'target':chemicalIndex,'weight':ADJ_sign[diseaseIndex,chemicalIndex]})
					
	NodeEdges = {'nodes':nodes,'edges':edges}
	return(NodeEdges)
