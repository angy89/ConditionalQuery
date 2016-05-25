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
	for nn in range(len(nanoOrigin)):
		nodes.append({'id':nanoOrigin[nn],'label':elemName[nn],'type':'nano'})
		
	for dd in range(len(drugOrigin)):
		nodes.append({'id':nanoOrigin[dd],'label':elemName[dd],'type':'drug'})

	for di in range(len(diseaseOrigin)):
		nodes.append({'id':nanoOrigin[di],'label':elemName[di],'type':'disease'})

	for cc in range(len(chemicalOrigin)):
		nodes.append({'id':nanoOrigin[cc],'label':elemName[cc],'type':'chemical'})
	
	edges = []
	
	for nn in range(len(nanoPos)):
		nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
		for dd in range(len(drugPos)):
			drugIndex = drugOrigin[drug.index(drugPos[dd])]
			nano_drug = NN_ADJ_red[nanoPos[nn],drugPos[dd]]!=0
			if(nano_drug):
				edges.append({'source':nanoIndex,'target':drugIndex,'weight':NN_ADJ_red[nanoPos[nn],drugPos[dd]]})
			for di in range(len(diseasePos)):
				diseaseIndex = diseaseOrigin[disease.index(diseasePos[di])]
				nano_disease = NN_ADJ_red[nanoPos[nn],diseasePos[di]]!=0
				
				if(nano_disease):
					edges.append({'source':nanoIndex,'target':diseaseIndex,'weight':NN_ADJ_red[nanoPos[nn],diseasePos[di]]})
				
				drug_disease = NN_ADJ_red[drugPos[dd],diseasePos[di]]!=0
				if(drug_disease):
					edges.append({'source':drugIndex,'target':diseaseIndex,'weight':NN_ADJ_red[drugPos[dd],diseasePos[di]]})
				for cc in range(len(chemicalPos)):
					chemicalIndex = chemicalOrigin[chemical.index(chemicalPos[cc])]	
					
					nano_chemical = NN_ADJ_red[nanoPos[nn],chemicalPos[cc]]!=0
					if(nano_chemical):
						edges.append({'source':nanoIndex,'target':chemicalIndex,'weight':NN_ADJ_red[nanoPos[nn],chemicalPos[cc]]})
					
					drug_chemical = NN_ADJ_red[drugPos[dd],chemicalPos[cc]]!=0
					if(drug_chemical):
						edges.append({'source':drugIndex,'target':chemicalIndex,'weight':NN_ADJ_red[drugPos[dd],chemicalPos[cc]]})
					
					disease_chemical = NN_ADJ_red[diseasePos[di],chemicalPos[cc]]!=0
					if(disease_chemical):
						edges.append({'source':diseaseIndex,'target':chemicalIndex,'weight':NN_ADJ_red[diseasePos[di],chemicalPos[cc]]})
					
	NodeEdges = {'nodes':nodes,'edges':edges}
	return(NodeEdges)
