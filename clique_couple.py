import numpy as np

def searchNanoDrug_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	print ' In Search Clique 2'
	#Nano - Drug - Disease
	cliques_NDrDi = set()
	#Nano - Drug - Disase -Chemical
	cliques_NDrDiC = set()
	#Nano - Drug- Chemical
	cliques_NDrC = set()
	#Nano - Disease - Chemical
	cliques_NDiC = set()
	#Drug - Disase - Chemical
	cliques_DrDiC = set()

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

	#Couple Nano - Drug
	for nn in range(len(nanoPos)): #for each nano in the query input
		for dd in range(len(drugPos)): #for each drug in the query input
			nano_drug = NN_ADJ_red[nanoPos[nn],drugPos[dd]]!=0 #nano-drug connection (True/False)
			if(nano_drug):
				disease_adj = NN_ADJ_red[drugPos[dd],disease]!=0
				disease_adj = [d for d,b in zip(disease, disease_adj) if b]
				if(len(disease_adj)>0):
					for di in range(len(disease_adj)):
						nano_disease = NN_ADJ_red[nanoPos[nn],disease_adj[di]]!=0 #nano-disease connection
						drug_disease = NN_ADJ_red[drugPos[dd],disease_adj[di]]!=0 #drug-disease connection
						if(nano_drug & nano_disease & drug_disease):
							nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
							drugIndex = drugOrigin[drug.index(drugPos[dd])]
							diseaseIndex = diseaseOrigin[di]
							cliques_index = (nanoIndex,drugIndex,diseaseIndex)
							cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
							cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex]) #edges are in the order nano-drug, nano-disease,drug-disease
							cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges))
							chem_adj = NN_ADJ_red[disease_adj[di],chemical]!=0	
							chem_adj = [d for d,b in zip(chemical, chem_adj) if b]
							if(len(chem_adj)>0):
								for cc in range(len(chem_adj)):
									nano_chem = NN_ADJ_red[nanoPos[nn],chem_adj[cc]]!=0 #nano-chem connection
									drug_chemical = NN_ADJ_red[drugPos[dd],chem_adj[cc]]!=0 #drug-chem connection
									disease_chemical = NN_ADJ_red[disease_adj[di],chem_adj[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chem & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										chemicalIndex = chemicalOrigin[cc]
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_chemical & drug_chemical):
												cliques_index = (nanoIndex,drugIndex,chemicalIndex)
												cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
												cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
												cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
												
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
									
				chemical_adj = NN_ADJ_red[drugPos[dd],chemical]!=0
				chemical_adj = [d for d,b in zip(chemical, chemical_adj) if b]
				if(len(chemical_adj)>0):
					for cc in range(len(chemical_adj)):
						nano_chemical = NN_ADJ_red[nanoPos[nn],chemical_adj[cc]]!=0 #nano-disease connection
						drug_chemical = NN_ADJ_red[drugPos[dd],chemical_adj[cc]]!=0 #drug-disease connection
						if(nano_drug & nano_chemical & drug_chemical):
							nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
							drugIndex = drugOrigin[drug.index(drugPos[dd])]
							chemicalIndex = chemicalOrigin[cc]
							cliques_index = (nanoIndex,drugIndex,chemicalIndex)
							cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
							cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex]) #edges are in the order nano-drug, nano-chemical,drug-chemical
							cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
							disease_adj = NN_ADJ_red[chemical_adj[cc],disease]!=0	
							disease_adj = [d for d,b in zip(disease, disease_adj) if b]
							if(len(disease_adj)>0):
								for di in range(len(disease_adj)):
									nano_disease = NN_ADJ_red[nanoPos[nn],disease_adj[di]]!=0 #nano-chem connection
									drug_disease = NN_ADJ_red[drugPos[dd],disease_adj[di]]!=0 #drug-chem connection
									disease_chemical = NN_ADJ_red[disease_adj[di],chemical_adj[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										chemicalIndex = chemicalOrigin[cc]
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
											
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
										
	Cliques = {'NanoDrugDiseaseChemical':cliques_NDrDiC,'NanoDrugDisease':cliques_NDrDi,'NanoDrugChemical':cliques_NDrC,'NanoDiseaseChemical':cliques_NDiC,'DrugDiseaseChemical':cliques_DrDiC}
	return Cliques

def searchNanoDisease_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	print ' In Search Clique 2'
	#Nano - Drug - Disease
	cliques_NDrDi = set()
	#Nano - Drug - Disase -Chemical
	cliques_NDrDiC = set()
	#Nano - Drug- Chemical
	cliques_NDrC = set()
	#Nano - Disease - Chemical
	cliques_NDiC = set()
	#Drug - Disase - Chemical
	cliques_DrDiC = set()

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

	#Couple Nano - Disease
	for nn in range(len(nanoPos)): #for each nano in the query input
		for di in range(len(diseasePos)): #for each drug in the query input
			nano_disease = NN_ADJ_red[nanoPos[nn],diseasePos[di]]!=0 #nano-disease connection (True/False)
			if(nano_disease):
				drug_adj = NN_ADJ_red[diseasePos[di],drug]!=0
				drug_adj = [d for d,b in zip(drug, drug_adj) if b]
				if(len(drug_adj)>0):
					for dd in range(len(drug_adj)):
						nano_drug = NN_ADJ_red[nanoPos[nn],drug_adj[dd]]!=0 #nano-drug connection
						drug_disease = NN_ADJ_red[drug_adj[dd],diseasePos[di]]!=0 #disease-drug connection
						if(nano_disease & nano_drug & drug_disease):
							nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
							drugIndex = drugOrigin[dd]
							diseaseIndex = diseaseOrigin[disease.index(diseasePos[di])]
							cliques_index = (nanoIndex,drugIndex,diseaseIndex) #Clique NANO-DRUG-DISEASE
							cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
							cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])#edges are in the order nano-drug, nano-disease,drug-disease
							cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) 
							chem_adj = NN_ADJ_red[drug_adj[di],chemical]!=0	
							chem_adj = [d for d,b in zip(chemical, chem_adj) if b]
							if(len(chem_adj)>0):
								for cc in range(len(chem_adj)):
									nano_chemical = NN_ADJ_red[nanoPos[nn],chem_adj[cc]]!=0 #nano-chem connection
									drug_chemical = NN_ADJ_red[drug_adj[dd],chem_adj[cc]]!=0 #drug-chem connection
									disease_chemical = NN_ADJ_red[diseasePos[di],chem_adj[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										chemicalIndex = chemicalOrigin[cc]
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex) #Clique NANO-DRUG-DISEASE-CHEMICAL
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex]) #Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) 
										
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
											
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
										
											
				chemical_adj = NN_ADJ_red[diseasePos[di],chemical]!=0
				chemical_adj = [d for d,b in zip(chemical, chemical_adj) if b]
				if(len(chemical_adj)>0):
					for cc in range(len(chemical_adj)):
						nano_chemical = NN_ADJ_red[nanoPos[nn],chemical_adj[cc]]!=0 #nano-disease connection
						disease_chemical = NN_ADJ_red[diseasePos[di],chemical_adj[cc]]!=0 #drug-disease connection
						if(nano_disease & nano_chemical & disease_chemical):
							nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
							diseaseIndex = drugOrigin[disease.index(diseasePos[di])]
							chemicalIndex = chemicalOrigin[cc]
							cliques_index = (nanoIndex,diseaseIndex,chemicalIndex) #Clique NANO-DISEASE-CHEMICAL
							cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
							cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex]) 
							#edges are in the order nano-disese, nano-chemical,disease-chemical
							cliques_NDiC.add((cliques_index,cliques_names,cliques_edges))  
							drug_adj = NN_ADJ_red[chemical_adj[cc],drug]!=0
							drug_adj = [d for d,b in zip(drug, drug_adj) if b]
							if(len(drug_adj)>0):
								for dd in range(len(drug_adj)):
									nano_drug = NN_ADJ_red[nanoPos[nn],drug_adj[dd]]!=0 #nano-chem connection
									drug_disease = NN_ADJ_red[drug_adj[dd],diseasePos[di]]!=0 #drug-chem connection
									drug_chemical = NN_ADJ_red[drug_adj[dd],chemical_adj[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										drugIndex = drugOrigin[dd]
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
										
	Cliques = {'NanoDrugDiseaseChemical':cliques_NDrDiC,'NanoDrugDisease':cliques_NDrDi,'NanoDrugChemical':cliques_NDrC,'NanoDiseaseChemical':cliques_NDiC,'DrugDiseaseChemical':cliques_DrDiC}
	return Cliques

def searchNanoChemical_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	print ' In searchNanoChemical_2'
	#Nano - Drug - Disease
	cliques_NDrDi = set()
	#Nano - Drug - Disase -Chemical
	cliques_NDrDiC = set()
	#Nano - Drug- Chemical
	cliques_NDrC = set()
	#Nano - Disease - Chemical
	cliques_NDiC = set()
	#Drug - Disase - Chemical
	cliques_DrDiC = set()

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

	#Couple Nano - Chemical
	for nn in range(len(nanoPos)): #for each nano in the query input
		nanoIndex = nanoOrigin[nano.index(nanoPos[nn])]
		for cc in range(len(chemicalPos)): #for each drug in the query input
			chemicalIndex = chemicalOrigin[chemical.index(chemicalPos[cc])]
			nano_chemical = NN_ADJ_red[nanoPos[nn],chemicalPos[cc]]!=0 #nano-chemical connection (True/False)
			if(nano_chemical):
				drug_adj = NN_ADJ_red[chemicalPos[cc],drug]!=0
				drug_adj = [d for d,b in zip(drug, drug_adj) if b]
				if(len(drug_adj)>0):
					for dd in range(len(drug_adj)):
						drugIndex = drugOrigin[dd]
						nano_drug = NN_ADJ_red[nanoPos[nn],drug_adj[dd]]!=0 #nano-drug connection
						drug_chemical = NN_ADJ_red[chemicalPos[cc],drug_adj[dd]]!=0 #disease-drug connection
						if(nano_chemical & nano_drug & drug_chemical):
							cliques_index = (nanoIndex,drugIndex,chemicalIndex) #Clique NANO-DRUG-CHEMICAL
							cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
							#Edges are in te order nano-drug, nano-chem, drug-chem
							cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex])
							cliques_NDrC.add((cliques_index,cliques_names,cliques_edges))
							disease_adj = NN_ADJ_red[drug_adj[dd],disease]!=0	
							disease_adj = [d for d,b in zip(disease, disease_adj) if b]
							if(len(disease_adj)>0):
								for di in range(len(disease_adj)):
									diseaseIndex = diseaseOrigin[di]
									nano_disease = NN_ADJ_red[nanoPos[nn],disease_adj[di]]!=0 #nano-chem connection
									drug_disease = NN_ADJ_red[drug_adj[dd],disease_adj[di]]!=0 #drug-chem connection
									disease_chemical = NN_ADJ_red[disease_adj[di],chemicalPos[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
										
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
										
				disease_adj = NN_ADJ_red[chemicalPos[cc],disease]!=0
				disease_adj = [d for d,b in zip(disease, disease_adj) if b]
				if(len(disease_adj)>0):
					for di in range(len(disease_adj)):
						diseaseIndex = diseaseOrigin[di]
						nano_disease = NN_ADJ_red[nanoPos[nn],disease_adj[di]]!=0 #nano-disease connection
						disease_chemical = NN_ADJ_red[chemicalPos[cc],disease_adj[di]]!=0 #drug-disease connection
						if(nano_disease & nano_chemical & disease_chemical):
							cliques_index = (nanoIndex,diseaseIndex,chemicalIndex) #NANO - DISEASE - CHEMICAL
							cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
							cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
							#edges are in the order nano-disease, nano-chem, disease-chem
							cliques_NDiC.add((cliques_index,cliques_names,cliques_edges))
							drug_adj = NN_ADJ_red[disease_adj[di],drug]!=0	
							drug_adj = [d for d,b in zip(drug, drug_adj) if b]
							if(len(drug_adj)>0):
								for dd in range(len(drug_adj)):
									drugIndex = drugOrigin[dd]
									nano_drug = NN_ADJ_red[nanoPos[nn],drug_adj[cc]]!=0 #nano-chem connection
									drug_chemical = NN_ADJ_red[drug_adj[dd],chemicalPos[cc]]!=0 #drug-chem connection
									drug_disease = NN_ADJ_red[disease_adj[di],drug_adj[dd]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
										
	Cliques = {'NanoDrugDiseaseChemical':cliques_NDrDiC,'NanoDrugDisease':cliques_NDrDi,'NanoDrugChemical':cliques_NDrC,'NanoDiseaseChemical':cliques_NDiC,'DrugDiseaseChemical':cliques_DrDiC}
	return Cliques

def searchDrugDisease_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	print ' In searchDrugDisease_2'
	#Nano - Drug - Disease
	cliques_NDrDi = set()
	#Nano - Drug - Disase -Chemical
	cliques_NDrDiC = set()
	#Nano - Drug- Chemical
	cliques_NDrC = set()
	#Nano - Disease - Chemical
	cliques_NDiC = set()
	#Drug - Disase - Chemical
	cliques_DrDiC = set()

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

	#Couple Drug - Disease
	for dd in range(len(drugPos)): #for each nano in the query input
		drugIndex = drugOrigin[drug.index(drugPos[dd])]
		for di in range(len(diseasePos)): #for each drug in the query input
			diseaseIndex = diseaseOrigin[disease.index(diseasePos[di])]
			drug_disease = NN_ADJ_red[drugPos[dd],diseasePos[di]]!=0 #nano-chemical connection (True/False)
			if(drug_disease):
				nano_adj = NN_ADJ_red[diseasePos[di],nano]!=0
				nano_adj = [d for d,b in zip(nano, nano_adj) if b]
				if(len(nano_adj)>0):
					for nn in range(len(nano_adj)):
						nanoIndex = nanoOrigin[nn]
						nano_drug = NN_ADJ_red[nano_adj[nn],drugPos[dd]]!=0 #nano-drug connection
						nano_disease = NN_ADJ_red[nano_adj[nn],diseasePos[di]]!=0 #disease-drug connection
						if(drug_disease & nano_drug & nano_disease):
							cliques_index = (nanoIndex,drugIndex,diseaseIndex)
							cliques_names = ((elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex]))
							#edges are in the order nano-drug, nano-disease,drug-disease
							cliques_edges= ((ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex]))
							cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
							chem_adj = NN_ADJ_red[nano_adj[di],chemical]!=0	
							chem_adj = [d for d,b in zip(chemical, chem_adj) if b]
							if(len(chem_adj)>0):
								for cc in range(len(chem_adj)):
									chemicalIndex = chemicalOrigin[cc]
									drug_chemical = NN_ADJ_red[drugPos[dd],chem_adj[cc]]!=0 #nano-chem connection
									disease_chemical = NN_ADJ_red[diseasePos[di],chem_adj[cc]]!=0 #drug-chem connection
									nano_chemical = NN_ADJ_red[nano_adj[nn],chem_adj[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
											
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
										
				chemical_adj = NN_ADJ_red[diseasePos[di],chemical]!=0
				chemical_adj = [d for d,b in zip(chemical, chemical_adj) if b]
				if(len(chemical_adj)>0):
					for cc in range(len(chemical_adj)):
						chemicalIndex = chemicalOrigin[cc]
						drug_chemical = NN_ADJ_red[drugPos[dd],chemical_adj[cc]]!=0 #nano-disease connection
						disease_chemical = NN_ADJ_red[diseasePos[di],chemical_adj[cc]]!=0 #drug-disease connection
						if(drug_disease & drug_chemical & disease_chemical):
							cliques_index = (drugIndex,diseaseIndex,chemicalIndex) #Clique DRUG-DISEASE-CHEMICAL
							cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
							cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex]) 
							#edges are in the order durg-disese, drug-chemical,disease-chemical
							cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) 
							nano_adj = NN_ADJ_red[chemical_adj[cc],nano]!=0
							nano_adj = [d for d,b in zip(nano, nano_adj) if b]
							if(len(nano_adj)>0):
								for nn in range(len(nano_adj)):
									nanoIndex = nano_adj[nn]
									nano_drug = NN_ADJ_red[nano_adj[nn],drugPos[dd]]!=0 #nano-chem connection
									nano_disease = NN_ADJ_red[nano_adj[nn],diseasePos[di]]!=0 #drug-chem connection
									nano_chemical = NN_ADJ_red[nano_adj[nn],chemical_adj[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
											
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
											
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
										
	Cliques = {'NanoDrugDiseaseChemical':cliques_NDrDiC,'NanoDrugDisease':cliques_NDrDi,'NanoDrugChemical':cliques_NDrC,'NanoDiseaseChemical':cliques_NDiC,'DrugDiseaseChemical':cliques_DrDiC}
	return Cliques


def searchDrugChemical_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	print ' In searchDrugChemical_2'
	#Nano - Drug - Disease
	cliques_NDrDi = set()
	#Nano - Drug - Disase -Chemical
	cliques_NDrDiC = set()
	#Nano - Drug- Chemical
	cliques_NDrC = set()
	#Nano - Disease - Chemical
	cliques_NDiC = set()
	#Drug - Disase - Chemical
	cliques_DrDiC = set()

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

	#Couple Drug - Chemical
	for dd in range(len(drugPos)):
		drugIndex = drugOrigin[drug.index(drugPos[dd])]
		for cc in range(len(chemicalPos)):
			chemicalIndex = chemicalOrigin[chemical.index(chemicalPos[cc])]
			drug_chemical = NN_ADJ_red[drugPos[dd],chemicalPos[cc]]!=0
			if(drug_chemical):
				nano_adj = NN_ADJ_red[chemicalPos[cc],nano]!=0
				nano_adj = [d for d,b in zip(nano, nano_adj) if b]
				if(len(nano_adj)>0):
					for nn in range(len(nano_adj)):
						nanoIndex = nanoOrigin[nn]
						nano_drug = NN_ADJ_red[nano_adj[nn],drugPos[dd]]!=0 #nano-drug connection
						nano_chemical = NN_ADJ_red[nano_adj[nn],chemicalPos[cc]]!=0
						if(drug_chemical & nano_drug & nano_chemical):
							cliques_index = (nanoIndex,drugIndex,chemicalIndex)#Clique NANO-DRUG-CHEMICAL
							cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
							#Edges are in te order nano-drug, nano-chem, drug-chem
							cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex])
							cliques_NDrC.add((cliques_index,cliques_names,cliques_edges))
							disease_adj = NN_ADJ_red[nano_adj[nn],disease]!=0	
							disease_adj = [d for d,b in zip(disease, disease_adj) if b]
							if(len(disease_adj)>0):
								for di in range(len(disease_adj)):
									diseaseIndex = diseaseOrigin[di]
									nano_disease = NN_ADJ_red[nano_adj[nn],disease_adj[di]]!=0 #nano-chem connection
									drug_disease = NN_ADJ_red[drugPos[dd],disease_adj[di]]!=0 #drug-chem connection
									disease_chemical = NN_ADJ_red[disease_adj[di],chemicalPos[cc]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
										
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
											
				disease_adj = NN_ADJ_red[chemicalPos[cc],disease]!=0
				disease_adj = [d for d,b in zip(disease, disease_adj) if b]
				if(len(disease_adj)>0):
					for di in range(len(disease_adj)):
						diseaseIndex = diseaseOrigin[di]
						drug_disease = NN_ADJ_red[drugPos[dd],disease_adj[di]]!=0 #nano-disease connection
						disease_chemical = NN_ADJ_red[chemicalPos[cc],disease_adj[di]]!=0 #drug-disease connection
						if(drug_disease & drug_chemical & disease_chemical):
							cliques_index = (drugIndex,diseaseIndex,chemicalIndex) #DRUG - DISEASE - CHEMICAL
							cliques_names = ((elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex]))
							cliques_edges = ((ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])) 
							#edges are in the order dug-disease, drug-chem, disease-chem
							cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges))
							nano_adj = NN_ADJ_red[disease_adj[di],nano]!=0
							nano_adj = [d for d,b in zip(nano, nano_adj) if b]
							if(len(nano_adj)>0):
								for nn in range(len(nano_adj)):
									nanoIndex = nanoOrigin[nn]
									nano_drug = NN_ADJ_red[nano_adj[nn],drugPos[dd]]!=0 #nano-chem connection
									nano_chemical = NN_ADJ_red[nano_adj[nn],chemicalPos[cc]]!=0 #drug-chem connection
									nano_disease = NN_ADJ_red[disease_adj[di],nano_adj[nn]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
										
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
											
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
										
	Cliques = {'NanoDrugDiseaseChemical':cliques_NDrDiC,'NanoDrugDisease':cliques_NDrDi,'NanoDrugChemical':cliques_NDrC,'NanoDiseaseChemical':cliques_NDiC,'DrugDiseaseChemical':cliques_DrDiC}
	return Cliques

def searchDiseaseChemical_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
	print ' In searchDiseaseChemical_2'
	#Nano - Drug - Disease
	cliques_NDrDi = set()
	#Nano - Drug - Disase -Chemical
	cliques_NDrDiC = set()
	#Nano - Drug- Chemical
	cliques_NDrC = set()
	#Nano - Disease - Chemical
	cliques_NDiC = set()
	#Drug - Disase - Chemical
	cliques_DrDiC = set()

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

	#Couple Disease - Chemical
	for di in range(len(diseasePos)):
		diseaseIndex = diseaseOrigin[disease.index(diseasePos[di])]
		for cc in range(len(chemicalPos)):
			chemicalIndex = chemicalOrigin[chemical.index(chemicalPos[cc])]
			disease_chemical = NN_ADJ_red[diseasePos[di],chemicalPos[cc]]!=0
			if(disease_chemical):
				nano_adj = NN_ADJ_red[chemicalPos[cc],nano]!=0
				nano_adj = [d for d,b in zip(nano, nano_adj) if b]
				if(len(nano_adj)>0):
					for nn in range(len(nano_adj)):
						nanoIndex = nanoOrigin[nn]
						nano_disease = NN_ADJ_red[nano_adj[nn],diseasePos[di]]!=0 #nano-drug connection
						nano_chemical = NN_ADJ_red[nano_adj[nn],chemicalPos[cc]]!=0
						if(nano_chemical & nano_disease & disease_chemical):
							cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
							cliques_names = ((elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex]))
							cliques_edges = ((ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])) 
							cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
							drug_adj = NN_ADJ_red[nano_adj[di],drug]!=0	
							drug_adj = [d for d,b in zip(drug, drug_adj) if b]
							if(len(drug_adj)>0):
								for dd in range(len(drug_adj)):
									drugIndex = drugOrigin[dd]
									nano_drug = NN_ADJ_red[nano_adj[nn],drug_adj[dd]]!=0 #nano-chem connection
									drug_disease = NN_ADJ_red[diseasePos[di],drug_adj[dd]]!=0 #drug-chem connection
									drug_chemical = NN_ADJ_red[chemicalPos[cc],drug_adj[dd]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
											
										if(drug_disease & drug_chemical & disease_chemical):
											cliques_index = (drugIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique DRUG-DISEASE-CHEMICAL
										
				drug_adj = NN_ADJ_red[chemicalPos[cc],drug]!=0
				drug_adj = [d for d,b in zip(drug, drug_adj) if b]
				if(len(drug_adj)>0):
					for dd in range(len(drug_adj)):
						drugIndex = drugOrigin[dd]
						drug_disease = NN_ADJ_red[diseasePos[di],drug_adj[dd]]!=0 #nano-drug connection
						drug_chemical = NN_ADJ_red[chemicalPos[cc],drug_adj[dd]]!=0 #disease-drug connection
						if(drug_disease & disease_chemical & drug_chemical):
							cliques_index = (drugIndex,diseaseIndex,chemicalIndex) #Clique -DRUG-DISEASE-CHEMICAL
							cliques_names = (elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
							#Edges are in te order drug-disease drug-chem, disea-chem
							cliques_edges = (ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
							cliques_DrDiC.add((cliques_index,cliques_names,cliques_edges))
							nano_adj = NN_ADJ_red[drug_adj[dd],nano]!=0
							nano_adj = [d for d,b in zip(nano, nano_adj) if b]
							if(len(nano_adj)>0):
								for nn in range(len(nano_adj)):
									nanoIndex = nanoOrigin[nn]
									nano_drug = NN_ADJ_red[nano_adj[nn],drug_adj[dd]]!=0 #nano-chem connection
									nano_chemical = NN_ADJ_red[nano_adj[nn],chemicalPos[cc]]!=0 #drug-chem connection
									nano_disease = NN_ADJ_red[diseasePos[di],nano_adj[nn]]!=0 #chem-disease connection
									isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
									if(isClique):
										cliques_index = (nanoIndex,drugIndex,diseaseIndex,chemicalIndex)
										cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex],elemName[chemicalIndex])
										#Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
										cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,diseaseIndex],ADJ_sign[drugIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
										cliques_NDrDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE-CHEMICAL
										
										if(nano_drug & nano_disease & drug_disease):
											cliques_index = (nanoIndex,drugIndex,diseaseIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[diseaseIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[drugIndex,diseaseIndex])
											cliques_NDrDi.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-DISEASE
										
										if(nano_disease & nano_chemical & disease_chemical):
											cliques_index = (nanoIndex,diseaseIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[diseaseIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,diseaseIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[diseaseIndex,chemicalIndex])
											cliques_NDiC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DISEASE-CHEMICAL
											
										if(nano_drug & nano_chemical & drug_chemical):
											cliques_index = (nanoIndex,drugIndex,chemicalIndex)
											cliques_names = (elemName[nanoIndex],elemName[drugIndex],elemName[chemicalIndex])
											cliques_edges = (ADJ_sign[nanoIndex,drugIndex],ADJ_sign[nanoIndex,chemicalIndex],ADJ_sign[drugIndex,chemicalIndex] )
											cliques_NDrC.add((cliques_index,cliques_names,cliques_edges)) #Clique NANO-DRUG-CHEMICAL
	
	Cliques = {'NanoDrugDiseaseChemical':cliques_NDrDiC,'NanoDrugDisease':cliques_NDrDi,'NanoDrugChemical':cliques_NDrC,'NanoDiseaseChemical':cliques_NDiC,'DrugDiseaseChemical':cliques_DrDiC}
	return Cliques

