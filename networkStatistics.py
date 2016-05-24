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
