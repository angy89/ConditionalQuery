import numpy as np


def searchNanoDrug_2(NN_ADJ, ADJ_sign, ADJ_known,nano, drug, chemical, disease, queryInput, elemName):
    # Nano - Drug - Disease
    cliques_NDrDi = set()
    # Nano - Drug - Disase -Chemical
    cliques_NDrDiC = set()
    # Nano - Drug- Chemical
    cliques_NDrC = set()
    # Nano - Disease - Chemical
    cliques_NDiC = set()
    # Drug - Disase - Chemical
    cliques_DrDiC = set()

    nanoInput = queryInput['nano']
    drugInput = queryInput['drug']

    for nn in range(len(nanoInput)):
        nanoIndex = nanoInput[nn]
        for dd in range(len(drugInput)):
            drugIndex = drugInput[dd]
            nano_drug = NN_ADJ[nanoInput[nn], drugInput[dd]] != 0  # nano-drug connection (True/False)
            if (nano_drug):
                disease_adj = NN_ADJ[drugInput[dd], :] * disease != 0
                if (np.sum(disease_adj) > 0):
                    disease_adj = [d for d in np.where(disease_adj == True)[0]]
                    for di in range(len(disease_adj)):
                        nano_disease = NN_ADJ[nanoIndex, disease_adj[di]] != 0  # nano-disease connection
                        drug_disease = NN_ADJ[drugIndex, disease_adj[di]] != 0  # drug-disease connection
                        if (nano_drug & nano_disease & drug_disease):
                            diseaseIndex = disease_adj[di]
                            cliques_index = (nanoIndex, drugIndex, diseaseIndex)
                            cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex])
                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],ADJ_sign[drugIndex, diseaseIndex])  # edges are in the order nano-drug, nano-disease,drug-disease
                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],ADJ_known[drugIndex, diseaseIndex])  # edges are in the order nano-drug, nano-disease,drug-disease
                            cliques_NDrDi.add((cliques_index, cliques_names, cliques_edges,known_edges))
                            chemical_adj = NN_ADJ[disease_adj[di], :] * chemical != 0
                            if (np.sum(chemical_adj) > 0):
                                chemical_adj = [d for d in np.where(chemical_adj == True)[0]]
                                for cc in range(len(chemical_adj)):
                                    nano_chem = NN_ADJ[nanoIndex, chemical_adj[cc]] != 0  # nano-chem connection
                                    drug_chemical = NN_ADJ[drugIndex, chemical_adj[cc]] != 0  # drug-chem connection
                                    disease_chemical = NN_ADJ[diseaseIndex, chemical_adj[
                                        cc]] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chem & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        chemicalIndex = chemical_adj[cc]
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])  # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        known_edges = (
                                        ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (nano_drug & nano_chem & drug_chemical):
                                            cliques_index = (nanoIndex, drugIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[drugIndex, chemicalIndex])
                                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[drugIndex, chemicalIndex])
                                            cliques_NDrC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL

                chemical_adj = NN_ADJ[drugInput[dd], :] * chemical != 0
                if (np.sum(chemical_adj) > 0):
                    chemical_adj = [d for d in np.where(chemical_adj == True)[0]]
                    for cc in range(len(chemical_adj)):
                        nano_chemical = NN_ADJ[nanoIndex, chemical_adj[cc]] != 0  # nano-disease connection
                        drug_chemical = NN_ADJ[drugIndex, chemical_adj[cc]] != 0  # drug-disease connection
                        if (nano_drug & nano_chemical & drug_chemical):
                            chemicalIndex = chemical_adj[cc]
                            cliques_index = (nanoIndex, drugIndex, chemicalIndex)
                            cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[drugIndex, chemicalIndex])  # edges are in the order nano-drug, nano-chemical,drug-chemical
                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[drugIndex, chemicalIndex])
                            cliques_NDrC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL
                            disease_adj = NN_ADJ[chemical_adj[cc], :] * disease != 0
                            if (np.sum(disease_adj) > 0):
                                disease_adj = [d for d in np.where(disease_adj == True)[0]]
                                for di in range(len(disease_adj)):
                                    nano_disease = NN_ADJ[nanoIndex, disease_adj[di]] != 0  # nano-chem connection
                                    drug_disease = NN_ADJ[drugIndex, disease_adj[di]] != 0  # drug-chem connection
                                    disease_chemical = NN_ADJ[disease_adj[di], chemicalIndex] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        diseaseIndex = disease_adj[di]
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (
                                        ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (nano_drug & nano_disease & drug_disease):
                                            cliques_index = (nanoIndex, drugIndex, diseaseIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex])
                                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],ADJ_sign[drugIndex, diseaseIndex])
                                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],ADJ_known[drugIndex, diseaseIndex])
                                            cliques_NDrDi.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE

    Cliques = {'NanoDrugDiseaseChemical': cliques_NDrDiC, 'NanoDrugDisease': cliques_NDrDi,
               'NanoDrugChemical': cliques_NDrC, 'NanoDiseaseChemical': cliques_NDiC,
               'DrugDiseaseChemical': cliques_DrDiC}
    return Cliques


def searchNanoDisease_2(NN_ADJ, ADJ_sign,ADJ_known, nano, drug, chemical, disease, queryInput, elemName):
    # Nano - Drug - Disease
    cliques_NDrDi = set()
    # Nano - Drug - Disase -Chemical
    cliques_NDrDiC = set()
    # Nano - Drug- Chemical
    cliques_NDrC = set()
    # Nano - Disease - Chemical
    cliques_NDiC = set()
    # Drug - Disase - Chemical
    cliques_DrDiC = set()

    nanoInput = queryInput['nano']
    diseaseInput = queryInput['disease']

    # Couple Nano - Disease
    for nn in range(len(nanoInput)):
        nanoIndex = nanoInput[nn]
        for di in range(len(diseaseInput)):
            diseaseIndex = diseaseInput[di]
            nano_disease = NN_ADJ[nanoInput[nn], diseaseInput[di]] != 0  # nano-drug connection (True/False)
            if (nano_disease):
                drug_adj = NN_ADJ[diseaseInput[di], :] * drug != 0
                if (np.sum(drug_adj) > 0):
                    drug_adj = [d for d in np.where(drug_adj == True)[0]]
                    for dd in range(len(drug_adj)):
                        nano_drug = NN_ADJ[nanoIndex, drug_adj[dd]] != 0  # nano-drug connection
                        drug_disease = NN_ADJ[drug_adj[dd], diseaseIndex] != 0  # disease-drug connection
                        if (nano_disease & nano_drug & drug_disease):
                            drugIndex = drug_adj[dd]
                            cliques_index = (nanoIndex, drugIndex, diseaseIndex)  # Clique NANO-DRUG-DISEASE
                            cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex])
                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],ADJ_sign[drugIndex, diseaseIndex])  # edges are in the order nano-drug, nano-disease,drug-disease
                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],ADJ_known[drugIndex, diseaseIndex])
                            cliques_NDrDi.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE
                            chemical_adj = NN_ADJ[drug_adj[dd], :] * chemical != 0
                            if (np.sum(chemical_adj) > 0):
                                chemical_adj = [d for d in np.where(chemical_adj == True)[0]]
                                for cc in range(len(chemical_adj)):
                                    nano_chem = NN_ADJ[nanoIndex, chemical_adj[cc]] != 0  # nano-chem connection
                                    drug_chemical = NN_ADJ[drugIndex, chemical_adj[cc]] != 0  # drug-chem connection
                                    disease_chemical = NN_ADJ[diseaseIndex, chemical_adj[cc]] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chem & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        chemicalIndex = chemical_adj[cc]
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])  # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE
                                        if (nano_disease & nano_chem & disease_chemical):
                                            cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                                            known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                                            cliques_NDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL

                chemical_adj = NN_ADJ[diseaseInput[di], :] * chemical != 0
                if (np.sum(chemical_adj) > 0):
                    chemical_adj = [d for d in np.where(chemical_adj == True)[0]]
                    for cc in range(len(chemical_adj)):
                        nano_chemical = NN_ADJ[nanoIndex, chemical_adj[cc]] != 0  # nano-disease connection
                        disease_chemical = NN_ADJ[diseaseIndex, chemical_adj[cc]] != 0  # drug-disease connection
                        if (nano_disease & nano_chemical & disease_chemical):
                            chemicalIndex = chemical_adj[cc]
                            cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)  # Clique NANO-DISEASE-CHEMICAL
                            cliques_names = (elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                            cliques_edges = (ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                            # edges are in the order nano-disese, nano-chemical,disease-chemical
                            known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                            cliques_NDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL
                            drug_adj = NN_ADJ[chemical_adj[cc], :] * drug != 0
                            if (np.sum(drug_adj) > 0):
                                drug_adj = [d for d in np.where(drug_adj == True)[0]]
                                for dd in range(len(drug_adj)):
                                    nano_drug = NN_ADJ[nanoIndex, drug_adj[dd]] != 0  # nano-chem connection
                                    drug_disease = NN_ADJ[drug_adj[dd], diseaseIndex] != 0  # drug-chem connection
                                    drug_chemical = NN_ADJ[drug_adj[dd], chemicalIndex] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        drugIndex = drug_adj[dd]
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (nano_disease & nano_chemical & disease_chemical):
                                            cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                                            known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                                            cliques_NDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL

    Cliques = {'NanoDrugDiseaseChemical': cliques_NDrDiC, 'NanoDrugDisease': cliques_NDrDi,
               'NanoDrugChemical': cliques_NDrC, 'NanoDiseaseChemical': cliques_NDiC,
               'DrugDiseaseChemical': cliques_DrDiC}
    return Cliques


def searchNanoChemical_2(NN_ADJ, ADJ_sign, ADJ_known,nano, drug, chemical, disease, queryInput, elemName):
    # Nano - Drug - Disease
    cliques_NDrDi = set()
    # Nano - Drug - Disase -Chemical
    cliques_NDrDiC = set()
    # Nano - Drug- Chemical
    cliques_NDrC = set()
    # Nano - Disease - Chemical
    cliques_NDiC = set()
    # Drug - Disase - Chemical
    cliques_DrDiC = set()

    nanoInput = queryInput['nano']
    chemicalInput = queryInput['chemical']

    # Couple Nano - Chemical
    for nn in range(len(nanoInput)):
        nanoIndex = nanoInput[nn]
        for cc in range(len(chemicalInput)):
            chemicalIndex = chemicalInput[cc]
            nano_chemical = NN_ADJ[nanoInput[nn], chemicalInput[cc]] != 0  # nano-drug connection (True/False)
            if (nano_chemical):
                drug_adj = NN_ADJ[chemicalInput[cc], :] * drug != 0
                if (np.sum(drug_adj) > 0):
                    drug_adj = [d for d in np.where(drug_adj == True)[0]]
                    for dd in range(len(drug_adj)):
                        nano_drug = NN_ADJ[nanoIndex, drug_adj[dd]] != 0  # nano-drug connection
                        drug_chemical = NN_ADJ[drug_adj[dd], chemicalIndex] != 0  # disease-drug connection

                        if (nano_chemical & nano_drug & drug_chemical):
                            drugIndex = drug_adj[dd]
                            cliques_index = (nanoIndex, drugIndex, chemicalIndex)  # Clique NANO-DRUG-CHEMICAL
                            cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                            # Edges are in te order nano-drug, nano-chem, drug-chem
                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[drugIndex, chemicalIndex])
                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[drugIndex, chemicalIndex])
                            cliques_NDrC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL

                            disease_adj = NN_ADJ[drugIndex, :] * disease != 0
                            if (np.sum(disease_adj) > 0):
                                disease_adj = [d for d in np.where(disease_adj == True)[0]]
                                for di in range(len(disease_adj)):
                                    nano_disease = NN_ADJ[nanoIndex, disease_adj[di]] != 0  # nano-chem connection
                                    drug_disease = NN_ADJ[drugIndex, disease_adj[di]] != 0  # drug-chem connection
                                    disease_chemical = NN_ADJ[disease_adj[di], chemicalIndex] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        diseaseIndex = disease_adj[di]
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])

                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (nano_disease & nano_chemical & disease_chemical):
                                            cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                                            known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                                            cliques_NDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL
                disease_adj = NN_ADJ[chemicalInput[cc], :] * disease != 0
                if (np.sum(disease_adj) > 0):
                    disease_adj = [d for d in np.where(disease_adj == True)[0]]
                    for di in range(len(disease_adj)):
                        nano_disease = NN_ADJ[nanoIndex, disease_adj[di]] != 0  # nano-disease connection
                        disease_chemical = NN_ADJ[
                                               disease_adj[di], chemicalIndex] != 0  # drug-disease connection
                        if (nano_disease & nano_chemical & disease_chemical):
                            diseaseIndex = disease_adj[di]
                            cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)  # NANO - DISEASE - CHEMICAL
                            cliques_names = (elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                            cliques_edges = (ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                            # edges are in the order nano-disease, nano-chem, disease-chem
                            known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                            cliques_NDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL
                            drug_adj = NN_ADJ[disease_adj[di], :] * drug != 0
                            if (np.sum(drug_adj) > 0):
                                drug_adj = [d for d in np.where(drug_adj == True)[0]]
                                for dd in range(len(drug_adj)):
                                    drugIndex = drug_adj[dd]
                                    nano_drug = NN_ADJ[nanoIndex, drug_adj[dd]] != 0  # nano-chem connection
                                    drug_disease = NN_ADJ[drug_adj[dd], disease_adj[di]] != 0  # drug-chem connection
                                    drug_chemical = NN_ADJ[drug_adj[dd], chemicalIndex] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical

                                    if (isClique):
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (nano_drug & nano_chemical & drug_chemical):
                                            cliques_index = (nanoIndex, drugIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                                            cliques_edges = (
                                            ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                            ADJ_sign[drugIndex, chemicalIndex])
                                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[drugIndex, chemicalIndex])
                                            cliques_NDrC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL

    Cliques = {'NanoDrugDiseaseChemical': cliques_NDrDiC, 'NanoDrugDisease': cliques_NDrDi,
               'NanoDrugChemical': cliques_NDrC, 'NanoDiseaseChemical': cliques_NDiC,
               'DrugDiseaseChemical': cliques_DrDiC}
    return Cliques


def searchDrugDisease_2(NN_ADJ, ADJ_sign,ADJ_known, nano, drug, chemical, disease, queryInput, elemName):
    # Nano - Drug - Disease
    cliques_NDrDi = set()
    # Nano - Drug - Disase -Chemical
    cliques_NDrDiC = set()
    # Nano - Drug- Chemical
    cliques_NDrC = set()
    # Nano - Disease - Chemical
    cliques_NDiC = set()
    # Drug - Disase - Chemical
    cliques_DrDiC = set()

    drugInput = queryInput['drug']
    diseaseInput = queryInput['disease']

    # Couple Drug - Disease
    for dd in range(len(drugInput)):  # for each nano in the query input
        drugIndex = drugInput[dd]
        for di in range(len(diseaseInput)):  # for each drug in the query input
            diseaseIndex = diseaseInput[di]
            drug_disease = NN_ADJ[drugInput[dd], diseaseInput[di]] != 0

            if (drug_disease):
                nano_adj = NN_ADJ[diseaseInput[di], :] * nano != 0
                if (np.sum(nano_adj) > 0):
                    nano_adj = [d for d in np.where(nano_adj == True)[0]]
                    for nn in range(len(nano_adj)):
                        nanoIndex = nano_adj[nn]
                        nano_drug = NN_ADJ[nano_adj[nn], drugIndex] != 0  # nano-drug connection
                        nano_disease = NN_ADJ[nano_adj[nn], diseaseIndex] != 0  # disease-drug connection

                        if (drug_disease & nano_drug & nano_disease):
                            cliques_index = (nanoIndex, drugIndex, diseaseIndex)
                            cliques_names = ((elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex]))
                            # edges are in the order nano-drug, nano-disease,drug-disease
                            cliques_edges = ((ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],ADJ_sign[drugIndex, diseaseIndex]))
                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],ADJ_known[drugIndex, diseaseIndex])
                            cliques_NDrDi.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE
                            chem_adj = NN_ADJ[nanoIndex, :] * chemical != 0
                            if (np.sum(chem_adj) > 0):
                                chem_adj = [d for d in np.where(chem_adj == True)[0]]

                                for cc in range(len(chem_adj)):
                                    chemicalIndex = chem_adj[cc]
                                    drug_chemical = NN_ADJ[drugIndex, chem_adj[cc]] != 0  # nano-chem connection
                                    disease_chemical = NN_ADJ[diseaseIndex, chem_adj[cc]] != 0  # drug-chem connection
                                    nano_chemical = NN_ADJ[nano_adj[nn], chem_adj[cc]] != 0  # chem-disease connection

                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (drug_disease & drug_chemical & disease_chemical):
                                            cliques_index = (drugIndex, diseaseIndex, chemicalIndex)
                                            cliques_names = (elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                                            known_edges = (ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                                            cliques_DrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL

                chemical_adj = NN_ADJ[diseaseInput[di], :] * chemical != 0
                if (np.sum(chemical_adj) > 0):
                    chemical_adj = [d for d in np.where(chemical_adj == True)[0]]
                    for cc in range(len(chemical_adj)):
                        chemicalIndex = chemical_adj[cc]
                        drug_chemical = NN_ADJ[drugIndex, chemical_adj[cc]] != 0  # nano-disease connection
                        disease_chemical = NN_ADJ[diseaseIndex, chemical_adj[cc]] != 0  # drug-disease connection
                        if (drug_disease & drug_chemical & disease_chemical):
                            cliques_index = (drugIndex, diseaseIndex, chemicalIndex)  # Clique DRUG-DISEASE-CHEMICAL
                            cliques_names = (elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                            cliques_edges = (ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                            known_edges = (ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                            cliques_DrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL

                            nano_adj = NN_ADJ[diseaseInput[di], :] * nano != 0
                            if (np.sum(nano_adj) > 0):
                                nano_adj = [d for d in np.where(nano_adj == True)[0]]
                                for nn in range(len(nano_adj)):
                                    nanoIndex = nano_adj[nn]
                                    nano_drug = NN_ADJ[nano_adj[nn], drugIndex] != 0  # nano-chem connection
                                    nano_disease = NN_ADJ[nano_adj[nn], diseaseIndex] != 0  # drug-chem connection
                                    nano_chemical = NN_ADJ[nano_adj[nn], chemical_adj[cc]] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL
                                        if (nano_drug & nano_disease & drug_disease):
                                            cliques_index = (nanoIndex, drugIndex, diseaseIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex])
                                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],ADJ_sign[drugIndex, diseaseIndex])
                                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],ADJ_known[drugIndex, diseaseIndex])
                                            cliques_NDrDi.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE
    Cliques = {'NanoDrugDiseaseChemical': cliques_NDrDiC, 'NanoDrugDisease': cliques_NDrDi,
               'NanoDrugChemical': cliques_NDrC, 'NanoDiseaseChemical': cliques_NDiC,
               'DrugDiseaseChemical': cliques_DrDiC}
    return Cliques


def searchDrugChemical_2(NN_ADJ, ADJ_sign,ADJ_known, nano, drug, chemical, disease, queryInput, elemName):
    # Nano - Drug - Disease
    cliques_NDrDi = set()
    # Nano - Drug - Disase -Chemical
    cliques_NDrDiC = set()
    # Nano - Drug- Chemical
    cliques_NDrC = set()
    # Nano - Disease - Chemical
    cliques_NDiC = set()
    # Drug - Disase - Chemical
    cliques_DrDiC = set()

    drugInput = queryInput['drug']
    chemicalInput = queryInput['chemical']

    # Couple Drug - Chemical
    for dd in range(len(drugInput)):
        drugIndex = drugInput[dd]
        for cc in range(len(chemicalInput)):
            chemicalIndex = chemicalInput[cc]
            drug_chemical = NN_ADJ[drugIndex, chemicalIndex] != 0
            if (drug_chemical):
                nano_adj = NN_ADJ[chemicalIndex, :] * nano != 0
                if (np.sum(nano_adj) > 0):
                    nano_adj = [d for d in np.where(nano_adj == True)[0]]
                    for nn in range(len(nano_adj)):
                        nanoIndex = nano_adj[nn]
                        nano_drug = NN_ADJ[nano_adj[nn], drugIndex] != 0  # nano-drug connection
                        nano_chemical = NN_ADJ[nano_adj[nn], chemicalIndex] != 0  # disease-drug connection
                        if (drug_chemical & nano_drug & nano_chemical):
                            cliques_index = (nanoIndex, drugIndex, chemicalIndex)  # Clique NANO-DRUG-CHEMICAL
                            cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                            # Edges are in te order nano-drug, nano-chem, drug-chem
                            cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                             ADJ_sign[drugIndex, chemicalIndex])
                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[drugIndex, chemicalIndex])
                            cliques_NDrC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL

                            disease_adj = NN_ADJ[chemicalIndex, :] * disease != 0
                            if (np.sum(disease_adj) > 0):
                                disease_adj = [d for d in np.where(disease_adj == True)[0]]
                                for di in range(len(disease_adj)):
                                    diseaseIndex = disease_adj[di]
                                    nano_disease = NN_ADJ[nano_adj[nn], disease_adj[di]] != 0  # nano-chem connection
                                    drug_disease = NN_ADJ[drugIndex, disease_adj[di]] != 0  # drug-chem connection
                                    disease_chemical = NN_ADJ[disease_adj[di], chemicalIndex] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (drug_disease & drug_chemical & disease_chemical):
                                            cliques_index = (drugIndex, diseaseIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                                            known_edges = (ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                                            cliques_DrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL
                disease_adj = NN_ADJ[chemicalIndex, :] * disease != 0
                if (np.sum(disease_adj) > 0):
                    disease_adj = [d for d in np.where(disease_adj == True)[0]]
                    for di in range(len(disease_adj)):
                        diseaseIndex = disease_adj[di]

                        drug_disease = NN_ADJ[drugIndex, disease_adj[di]] != 0  # nano-disease connection
                        disease_chemical = NN_ADJ[disease_adj[di], chemicalIndex] != 0  # drug-disease connection
                        if (drug_disease & drug_chemical & disease_chemical):
                            cliques_index = (drugIndex, diseaseIndex, chemicalIndex)  # DRUG - DISEASE - CHEMICAL
                            cliques_names = ((elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex]))
                            cliques_edges = ((ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex]))
                            # edges are in the order dug-disease, drug-chem, disease-chem
                            known_edges = (ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                            cliques_DrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL

                            nano_adj = NN_ADJ[diseaseIndex, :] * nano != 0
                            if (np.sum(nano_adj) > 0):
                                nano_adj = [d for d in np.where(nano_adj == True)[0]]
                                for nn in range(len(nano_adj)):
                                    nanoIndex = nano_adj[nn]

                                    nano_drug = NN_ADJ[nanoIndex, drugIndex] != 0  # nano-chem connection
                                    nano_chemical = NN_ADJ[nanoIndex, chemicalIndex] != 0  # drug-chem connection
                                    nano_disease = NN_ADJ[diseaseIndex, nanoIndex] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (nano_drug & nano_chemical & drug_chemical):
                                            cliques_index = (nanoIndex, drugIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                                            cliques_edges = (
                                            ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                            ADJ_sign[drugIndex, chemicalIndex])
                                            known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[drugIndex, chemicalIndex])
                                            cliques_NDrC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL


    Cliques = {'NanoDrugDiseaseChemical': cliques_NDrDiC, 'NanoDrugDisease': cliques_NDrDi,
               'NanoDrugChemical': cliques_NDrC, 'NanoDiseaseChemical': cliques_NDiC,
               'DrugDiseaseChemical': cliques_DrDiC}
    return Cliques


def searchDiseaseChemical_2(NN_ADJ, ADJ_sign,ADJ_known, nano, drug, chemical, disease, queryInput, elemName):
    # Nano - Drug - Disease
    cliques_NDrDi = set()
    # Nano - Drug - Disase -Chemical
    cliques_NDrDiC = set()
    # Nano - Drug- Chemical
    cliques_NDrC = set()
    # Nano - Disease - Chemical
    cliques_NDiC = set()
    # Drug - Disase - Chemical
    cliques_DrDiC = set()

    diseaseInput = queryInput['disease']
    chemicalInput = queryInput['chemical']

    # Couple Disease - Chemical
    for di in range(len(diseaseInput)):
        diseaseIndex = diseaseInput[di]
        for cc in range(len(chemicalInput)):
            chemicalIndex = chemicalInput[cc]

            disease_chemical = NN_ADJ[diseaseIndex, chemicalIndex] != 0

            if (disease_chemical):
                nano_adj = NN_ADJ[chemicalIndex, :] * nano != 0
                if (np.sum(nano_adj) > 0):
                    nano_adj = [d for d in np.where(nano_adj == True)[0]]
                    for nn in range(len(nano_adj)):
                        nanoIndex = nano_adj[nn]

                        nano_disease = NN_ADJ[nano_adj[nn], diseaseIndex] != 0  # nano-drug connection
                        nano_chemical = NN_ADJ[nano_adj[nn], chemicalIndex] != 0
                        if (nano_chemical & nano_disease & disease_chemical):
                            cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)
                            cliques_names = ((elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex]))
                            cliques_edges = ((ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex]))
                            known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                            cliques_NDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL

                            # continuare
                            drug_adj = NN_ADJ[nanoIndex, :] * drug != 0
                            if (np.sum(drug_adj) > 0):
                                drug_adj = [d for d in np.where(drug_adj == True)[0]]
                                for dd in range(len(drug_adj)):
                                    drugIndex = drug_adj[dd]
                                    nano_drug = NN_ADJ[nanoIndex, drugIndex] != 0  # nano-chem connection
                                    drug_disease = NN_ADJ[diseaseIndex, drugIndex] != 0  # drug-chem connection
                                    drug_chemical = NN_ADJ[chemicalIndex, drugIndex] != 0  # chem-disease connection
                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (drug_disease & drug_chemical & disease_chemical):
                                            cliques_index = (drugIndex, diseaseIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                                            known_edges = (ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                                            cliques_DrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL
                drug_adj = NN_ADJ[chemicalIndex, :] * drug != 0
                if (np.sum(drug_adj) > 0):
                    drug_adj = [d for d in np.where(drug_adj == True)[0]]
                    for dd in range(len(drug_adj)):
                        drugIndex = drug_adj[dd]

                        drug_disease = NN_ADJ[diseaseIndex, drugIndex] != 0  # nano-drug connection
                        drug_chemical = NN_ADJ[drugIndex, chemicalIndex] != 0  # disease-drug connection

                        if (drug_disease & disease_chemical & drug_chemical):
                            cliques_index = (drugIndex, diseaseIndex, chemicalIndex)  # Clique -DRUG-DISEASE-CHEMICAL
                            cliques_names = (elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                            # Edges are in te order drug-disease drug-chem, disea-chem
                            cliques_edges = (ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                            known_edges = (ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                            cliques_DrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL
                            nano_adj = NN_ADJ[chemicalIndex, :] * nano != 0
                            if (np.sum(nano_adj) > 0):
                                nano_adj = [d for d in np.where(nano_adj == True)[0]]
                                for nn in range(len(nano_adj)):
                                    nanoIndex = nano_adj[nn]
                                    nano_drug = NN_ADJ[nanoIndex, drugIndex] != 0  # nano-chem connection
                                    nano_chemical = NN_ADJ[nanoIndex, chemicalIndex] != 0  # drug-chem connection
                                    nano_disease = NN_ADJ[nanoIndex, diseaseIndex] != 0  # chem-disease connection

                                    isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
                                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                        elemName[chemicalIndex])
                                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                        ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                        ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex]) 
                                        cliques_NDrDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                        if (nano_disease & nano_chemical & disease_chemical):
                                            cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)
                                            cliques_names = (
                                            elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                            cliques_edges = (ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],ADJ_sign[diseaseIndex, chemicalIndex])
                                            known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],ADJ_known[diseaseIndex, chemicalIndex])
                                            cliques_NDiC.add((cliques_index, cliques_names,cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL

    Cliques = {'NanoDrugDiseaseChemical': cliques_NDrDiC, 'NanoDrugDisease': cliques_NDrDi,
               'NanoDrugChemical': cliques_NDrC, 'NanoDiseaseChemical': cliques_NDiC,
               'DrugDiseaseChemical': cliques_DrDiC}
    return Cliques