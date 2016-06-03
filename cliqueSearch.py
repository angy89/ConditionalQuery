import numpy as np
from clique_couple import searchNanoDrug_2
from clique_couple import searchNanoDisease_2
from clique_couple import searchNanoChemical_2
from clique_couple import searchDrugDisease_2
from clique_couple import searchDrugChemical_2
from clique_couple import searchDiseaseChemical_2


def searchClique_2(NN_ADJ, ADJ_sign, ADJ_known,nNanoInput, nDrugInput, nChemicalInput, nDiseaseInput, nano, drug, chemical,
                   disease, queryInput, elemName):
    isNano = nNanoInput > 0
    isDrug = nDrugInput > 0
    isChemical = nChemicalInput > 0
    isDisease = nDiseaseInput > 0

    NanoDrug = {'NanoDrugDiseaseChemical': set(), 'NanoDrugDisease': set(), 'NanoDrugChemical': set(),
                'NanoDiseaseChemical': set(), 'DrugDiseaseChemical': set()}
    NanoDisease = {'NanoDrugDiseaseChemical': set(), 'NanoDrugDisease': set(), 'NanoDrugChemical': set(),
                   'NanoDiseaseChemical': set(), 'DrugDiseaseChemical': set()}
    NanoChemical = {'NanoDrugDiseaseChemical': set(), 'NanoDrugDisease': set(), 'NanoDrugChemical': set(),
                    'NanoDiseaseChemical': set(), 'DrugDiseaseChemical': set()}
    DrugDisease = {'NanoDrugDiseaseChemical': set(), 'NanoDrugDisease': set(), 'NanoDrugChemical': set(),
                   'NanoDiseaseChemical': set(), 'DrugDiseaseChemical': set()}
    ChemicalDrug = {'NanoDrugDiseaseChemical': set(), 'NanoDrugDisease': set(), 'NanoDrugChemical': set(),
                    'NanoDiseaseChemical': set(), 'DrugDiseaseChemical': set()}
    DiseaseChemical = {'NanoDrugDiseaseChemical': set(), 'NanoDrugDisease': set(), 'NanoDrugChemical': set(),
                       'NanoDiseaseChemical': set(), 'DrugDiseaseChemical': set()}

    if (isNano & isDrug):
        # NanoDrug = searchNanoDrug_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
        NanoDrug = searchNanoDrug_2(NN_ADJ, ADJ_sign, ADJ_known, nano, drug, chemical, disease, queryInput, elemName)

    if (isNano & isDisease):
        # NanoDisease = searchNanoDisease_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
        NanoDisease = searchNanoDisease_2(NN_ADJ, ADJ_sign, ADJ_known, nano, drug, chemical, disease, queryInput, elemName)

    if (isNano & isChemical):
        # NanoChemical = searchNanoChemical_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
        NanoChemical = searchNanoChemical_2(NN_ADJ, ADJ_sign, ADJ_known, nano, drug, chemical, disease, queryInput, elemName)

    if (isDrug & isDisease):
        # DrugDisease = searchDrugDisease_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
        DrugDisease = searchDrugDisease_2(NN_ADJ, ADJ_sign, ADJ_known, nano, drug, chemical, disease, queryInput, elemName)

    if (isChemical & isDrug):
        # ChemicalDrug = searchDrugChemical_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
        ChemicalDrug = searchDrugChemical_2(NN_ADJ, ADJ_sign, ADJ_known, nano, drug, chemical, disease, queryInput, elemName)

    if (isDisease & isChemical):
        # DiseaseChemical = searchDiseaseChemical_2(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName)
        DiseaseChemical = searchDiseaseChemical_2(NN_ADJ, ADJ_sign,ADJ_known,  nano, drug, chemical, disease, queryInput, elemName)

    Cliques_NDrDiC = NanoDrug['NanoDrugDiseaseChemical'].union(NanoDisease['NanoDrugDiseaseChemical'],
                                                               NanoChemical['NanoDrugDiseaseChemical'],
                                                               DrugDisease['NanoDrugDiseaseChemical'],
                                                               ChemicalDrug['NanoDrugDiseaseChemical'],
                                                               DiseaseChemical['NanoDrugDiseaseChemical'])
    Cliques_NDrDi = NanoDrug['NanoDrugDisease'].union(NanoDisease['NanoDrugDisease'], NanoChemical['NanoDrugDisease'],
                                                      DrugDisease['NanoDrugDisease'], ChemicalDrug['NanoDrugDisease'],
                                                      DiseaseChemical['NanoDrugDisease'])
    Cliques_NDrC = NanoDrug['NanoDrugChemical'].union(NanoDisease['NanoDrugChemical'], NanoChemical['NanoDrugChemical'],
                                                      DrugDisease['NanoDrugChemical'], ChemicalDrug['NanoDrugChemical'],
                                                      DiseaseChemical['NanoDrugChemical'])
    Cliques_NDiC = NanoDrug['NanoDiseaseChemical'].union(NanoDisease['NanoDiseaseChemical'],
                                                         NanoChemical['NanoDiseaseChemical'],
                                                         DrugDisease['NanoDiseaseChemical'],
                                                         ChemicalDrug['NanoDiseaseChemical'],
                                                         DiseaseChemical['NanoDiseaseChemical'])
    Cliques_DrDiC = NanoDrug['DrugDiseaseChemical'].union(NanoDisease['DrugDiseaseChemical'],
                                                          NanoChemical['DrugDiseaseChemical'],
                                                          DrugDisease['DrugDiseaseChemical'],
                                                          ChemicalDrug['DrugDiseaseChemical'],
                                                          DiseaseChemical['DrugDiseaseChemical'])

    Cliques = {'NanoDrugDiseaseChemical': list(Cliques_NDrDiC), 'NanoDrugDisease': list(Cliques_NDrDi),
               'NanoDrugChemical': list(Cliques_NDrC), 'NanoDiseaseChemical': list(Cliques_NDiC),
               'DrugDiseaseChemical': list(Cliques_DrDiC)}

    return Cliques


# It search for all the clique of three objects  of different classes (queryObject).
# If it find a clique then it try to extend it with an object of the 4th class
# def searchClique_3(NN_ADJ_red,ADJ_sign,nNanoInput,nDrugInput,nChemicalInput,nDiseaseInput,nano,drug,chemical,disease,nanoOrigin,drugOrigin,diseaseOrigin,chemicalOrigin,queryInput,elemName):
def searchClique_3(NN_ADJ, ADJ_sign, ADJ_known,nNanoInput, nDrugInput, nChemicalInput, nDiseaseInput, nano, drug, chemical,
                   disease, queryInput, elemName):
    cliques_NDrDi = set()
    cliques_NDrDiC = set()
    cliques_NDrC = set()
    cliques_NDiC = set()
    cliques_DrDiC = set()

    isNano = nNanoInput > 0
    isDrug = nDrugInput > 0
    isChemical = nChemicalInput > 0
    isDisease = nDiseaseInput > 0

    nanoInput = queryInput['nano']
    drugInput = queryInput['drug']
    diseaseInput = queryInput['disease']
    chemicalInput = queryInput['chemical']

    if (isNano & isDrug & isDisease):
         # Nano-Drug-Disease
        for nn in range(len(nanoInput)):  # for each nano in the query input
            nanoIndex = nanoInput[nn]
            for dd in range(len(drugInput)):  # for each drug in the query input
                drugIndex = drugInput[dd]
                nano_drug = NN_ADJ[nanoIndex, drugIndex] != 0  # nano-drug connection (True/False)
                for di in range(len(diseaseInput)):  # for each disease in the query input
                    diseaseIndex = diseaseInput[di]
                    nano_disease = NN_ADJ[nanoIndex, diseaseIndex] != 0  # nano-disease connection (True/False)
                    drug_disease = NN_ADJ[nanoIndex, drugIndex] != 0  # drug-disease connection (True/False)
                    if (nano_drug & nano_disease & drug_disease):  # check if nano - drug and disease form a clique
                        cliques_index = (nanoIndex, drugIndex, diseaseIndex)  # create the clique
                        cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex])
                        cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                         ADJ_sign[drugIndex, diseaseIndex])
                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                         ADJ_known[drugIndex, diseaseIndex])
                        cliques_NDrDi.add((cliques_index, cliques_names,
                                           cliques_edges,known_edges))  # NANO-DRUG-DISEASE #add the clique in the right list

                        chemical_adj = NN_ADJ[diseaseIndex, :] * chemical != 0
                        if (np.sum(chemical_adj) > 0):
                            chemical_adj = [d for d in np.where(chemical_adj == True)[0]]
                            for cc in range(len(chemical_adj)):
                                chemicalIndex = chemical_adj[cc]
                                nano_chem = NN_ADJ[nanoIndex, chemicalIndex] != 0  # nano-chem connection (True/False)
                                drug_chemical = NN_ADJ[
                                                    drugIndex, chemicalIndex] != 0  # drug-chem connection (True/False)
                                disease_chemical = NN_ADJ[
                                                       diseaseIndex, chemicalIndex] != 0  # chem-disease connection (True/False)

                                isClique = nano_drug & nano_disease & nano_chem & drug_disease & drug_chemical & disease_chemical
                                if (isClique):  # Check if nano - drug - chemical and disease form a clique
                                    cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                    cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                                     elemName[chemicalIndex])
                                    # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                    cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                                     ADJ_sign[nanoIndex, chemicalIndex],
                                                     ADJ_sign[drugIndex, diseaseIndex],
                                                     ADJ_sign[drugIndex, chemicalIndex],
                                                     ADJ_sign[diseaseIndex, chemicalIndex])
                                    known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex])

                                    cliques_NDrDiC.add((cliques_index, cliques_names,
                                                        cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

    if (isNano & isDrug & isChemical):
        # Nano-Drug-Chem
        for nn in range(len(nanoInput)):  # for nano
            nanoIndex = nanoInput[nn]
            for dd in range(len(drugInput)):  # for drug
                drugIndex = drugInput[dd]
                nano_drug = NN_ADJ[nanoIndex, drugIndex] != 0
                for cc in range(len(chemicalInput)):  # for chemical
                    chemicalIndex = chemicalInput[cc]

                    nano_chemical = NN_ADJ[nanoIndex, chemicalIndex] != 0
                    drug_chemical = NN_ADJ[drugIndex, chemicalIndex] != 0

                    if (nano_drug & nano_chemical & drug_chemical):

                        cliques_index = (nanoIndex, drugIndex, chemicalIndex)  # create the clique
                        cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                        cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                         ADJ_sign[drugIndex, chemicalIndex])
                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],
                                         ADJ_known[drugIndex, chemicalIndex])
                        cliques_NDrC.add((cliques_index, cliques_names,
                                          cliques_edges,known_edges))  # NANO-DRUG-CHEMICAL #add the clique in the right list

                        disease_adj = NN_ADJ[chemicalIndex, :] * disease != 0
                        if (np.sum(disease_adj) > 0):
                            disease_adj = [d for d in np.where(disease_adj == True)[0]]
                            for di in range(len(disease_adj)):
                                diseaseIndex = disease_adj[di]
                                nano_disease = NN_ADJ[nanoIndex, diseaseIndex] != 0  # nano-disease connection
                                drug_disease = NN_ADJ[drugIndex, diseaseIndex] != 0  # drug-disease connection
                                chemical_disease = NN_ADJ[chemicalIndex, diseaseIndex] != 0  # chem-disease connection
                                isClique = nano_drug & nano_disease & nano_chemical & drug_disease & drug_chemical & chemical_disease
                                if (isClique):
                                    cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                    cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                                     elemName[chemicalIndex])
                                    # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                    cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                                     ADJ_sign[nanoIndex, chemicalIndex],
                                                     ADJ_sign[drugIndex, diseaseIndex],
                                                     ADJ_sign[drugIndex, chemicalIndex],
                                                     ADJ_sign[diseaseIndex, chemicalIndex])
                                    known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex])

                                    cliques_NDrDiC.add((cliques_index, cliques_names,
                                                        cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

    if (isNano & isDisease & isChemical):
        # Nano-Dise-Chem
        for nn in range(len(nanoInput)):  # for nano
            nanoIndex = nanoInput[nn]
            for di in range(len(diseaseInput)):  # for drug
                diseaseIndex = diseaseInput[di]
                nano_disease = NN_ADJ[nanoIndex, diseaseIndex] != 0
                for cc in range(len(chemicalInput)):  # for chemical
                    chemicalIndex = chemicalInput[cc]
                    nano_chemical = NN_ADJ[nanoIndex, chemicalIndex] != 0
                    disease_chemical = NN_ADJ[diseaseIndex, chemicalIndex] != 0

                    if (nano_disease & nano_chemical & disease_chemical):

                        cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)  # create the clique
                        cliques_names = (elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                        cliques_edges = (ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                         ADJ_sign[diseaseIndex, chemicalIndex])
                        known_edges = (ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],
                                         ADJ_known[diseaseIndex, chemicalIndex])
                        cliques_NDiC.add((cliques_index, cliques_names,
                                          cliques_edges,known_edges))  # NANO-DISEASE-CHEMICAL #add the clique in the right list

                        drug_adj = NN_ADJ[chemicalIndex, :] * drug != 0
                        if (np.sum(drug_adj) > 0):
                            drug_adj = [d for d in np.where(drug_adj == True)[0]]
                            for dd in range(len(drug_adj)):
                                drugIndex = drug_adj[dd]
                                nano_drug = NN_ADJ[nanoIndex, drugIndex] != 0  # nano-drug connection
                                disease_drug = NN_ADJ[diseaseIndex, drugIndex] != 0  # drug-drug connection
                                chemical_drug = NN_ADJ[chemicalIndex, drugIndex] != 0  # chem-drug connection
                                isClique = nano_drug & nano_disease & nano_chemical & disease_drug & chemical_drug & disease_chemical
                                if (isClique):
                                    cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                    cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                                     elemName[chemicalIndex])
                                    # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                    cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                                     ADJ_sign[nanoIndex, chemicalIndex],
                                                     ADJ_sign[drugIndex, diseaseIndex],
                                                     ADJ_sign[drugIndex, chemicalIndex],
                                                     ADJ_sign[diseaseIndex, chemicalIndex])
                                    known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex])

                                    cliques_NDrDiC.add((cliques_index, cliques_names,
                                                        cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

    if (isDrug & isDisease & isChemical):
        # Drug-Disease-Chem
        for dd in range(len(drugInput)):  # for drug
            drugIndex = drugInput[dd]
            for di in range(len(diseaseInput)):  # for disease
                diseaseIndex = diseaseInput[di]
                drug_disease = NN_ADJ[drugIndex, diseaseIndex] != 0

                for cc in range(len(chemicalInput)):  # for chemical
                    chemicalIndex = chemicalInput[cc]

                    drug_chemical = NN_ADJ[drugIndex, chemicalIndex] != 0
                    disease_chemical = NN_ADJ[diseaseIndex, chemicalIndex] != 0

                    if (drug_disease & drug_chemical & disease_chemical):

                        cliques_index = (drugIndex, diseaseIndex, chemicalIndex)  # create the clique
                        cliques_names = (elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                        cliques_edges = (ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],
                                         ADJ_sign[diseaseIndex, chemicalIndex])
                        known_edges = (ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],
                                         ADJ_known[diseaseIndex, chemicalIndex])
                        cliques_DrDiC.add((cliques_index, cliques_names,
                                           cliques_edges,known_edges))  # DRUG-DISEASE-CHEMICAL #add the clique in the right list

                        nano_adj = NN_ADJ[chemicalIndex, :] * nano != 0
                        if (np.sum(nano_adj) > 0):
                            nano_adj = [d for d in np.where(nano_adj == True)[0]]
                            for nn in range(len(nano_adj)):
                                nanoIndex = nano_adj[nn]

                                drug_nano = NN_ADJ[drugIndex, nanoIndex] != 0  # nano-drug connection
                                disease_nano = NN_ADJ[diseaseIndex, nanoIndex] != 0  # drug-drug connection
                                chemical_nano = NN_ADJ[chemicalIndex, nanoIndex] != 0  # chem-drug connection
                                isClique = drug_nano & disease_nano & chemical_nano & drug_disease & drug_chemical & disease_chemical
                                if (isClique):
                                    cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                                    cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex],
                                                     elemName[chemicalIndex])
                                    # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                                    cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                                     ADJ_sign[nanoIndex, chemicalIndex],
                                                     ADJ_sign[drugIndex, diseaseIndex],
                                                     ADJ_sign[drugIndex, chemicalIndex],
                                                     ADJ_sign[diseaseIndex, chemicalIndex])
                                    known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                                        ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                                        ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex])
                                    cliques_NDrDiC.add((cliques_index, cliques_names,
                                                        cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

    Cliques = {'NanoDrugDiseaseChemical': list(cliques_NDrDiC), 'NanoDrugDisease': list(cliques_NDrDi),
               'NanoDrugChemical': list(cliques_NDrC), 'NanoDiseaseChemical': list(cliques_NDiC),
               'DrugDiseaseChemical': list(cliques_DrDiC)}

    return Cliques


# It check if at least one element of the query is in the clique
def checkClique_one(queryInput, clique):
    QI = [item for sublist in queryInput.values() for item in sublist]
    for i in range(len(clique)):
        if (clique[i] in QI):
            return True
    return False


# It looks for all cliques of four element between the input elements
def clique4(NN_ADJ, ADJ_sign,ADJ_known, queryInput, elemName):
    # Cliques Search obj
    cliques_NDrDiC = set()
    nano = queryInput['nano']
    drug = queryInput['drug']
    disease = queryInput['disease']
    chemical = queryInput['chemical']

    for nn in range(len(nano)):
        for dd in range(len(drug)):
            nano_drug = NN_ADJ[nano[nn], drug[dd]] != 0  # nano-drug connection
            for di in range(len(disease)):
                nano_disease = NN_ADJ[nano[nn], disease[di]] != 0  # nano-disease connection
                drug_disease = NN_ADJ[drug[dd], disease[di]] != 0  # drug-disease connection
                for cc in range(len(chemical)):
                    nano_chem = NN_ADJ[nano[nn], chemical[cc]] != 0  # nano-chem connection
                    drug_chemical = NN_ADJ[drug[dd], chemical[cc]] != 0  # drug-chem connection
                    disease_chemical = NN_ADJ[disease[di], chemical[cc]] != 0  # chem-disease connection
                    isClique = nano_drug & nano_disease & nano_chem & drug_disease & drug_chemical & disease_chemical
                    if (isClique):
                        nanoIndex = nano[nn]
                        drugIndex = drug[dd]
                        diseaseIndex = disease[di]
                        chemicalIndex = chemical[cc]
                        cliques_index = (nanoIndex, drugIndex, diseaseIndex, chemicalIndex)
                        cliques_names = (
                        elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                        # Clique Edges are in the order: nano-drug,nano-disease,nano-chem,drug-disea,drug-chem,disea-chem
                        cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                         ADJ_sign[nanoIndex, chemicalIndex], ADJ_sign[drugIndex, diseaseIndex],
                                         ADJ_sign[drugIndex, chemicalIndex], ADJ_sign[diseaseIndex, chemicalIndex])
                        known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                         ADJ_known[nanoIndex, chemicalIndex], ADJ_known[drugIndex, diseaseIndex],
                                         ADJ_known[drugIndex, chemicalIndex], ADJ_known[diseaseIndex, chemicalIndex])

                        cliques_NDrDiC.add(
                            (cliques_index, cliques_names, cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

    Cliques = {'NanoDrugDiseaseChemical': list(cliques_NDrDiC), 'NanoDrugDisease': [], 'NanoDrugChemical': [],
               'NanoDiseaseChemical': [], 'DrugDiseaseChemical': []}
    return Cliques


# Clique Search looks for all different kind of cliques in the subnetwork;
# it only check that at least one element between the query element is included in the clique
def cliqueSearch(NN_ADJ, ADJ_sign, ADJ_known,nano, drug, disease, chemical, queryInput, elemName):
    cliques_NDrDi = set()
    cliques_NDrDiC = set()
    cliques_NDrC = set()
    cliques_NDiC = set()
    cliques_DrDiC = set()

    nano = [d for d in np.where(nano == True)[0]]
    drug = [d for d in np.where(drug == True)[0]]
    disease = [d for d in np.where(disease == True)[0]]
    chemical = [d for d in np.where(chemical == True)[0]]

    if (len(nano) > 0):
        for nn in range(len(nano)):
            nanoIndex = nano[nn]
            drug_adj = NN_ADJ[nanoIndex, drug] != 0
            drug_adj = [d for d, b in zip(drug, drug_adj) if b]
            if (len(drug_adj) > 0):
                for dd in range(len(drug_adj)):
                    drugIndex = drug_adj[dd]
                    nano_drug = NN_ADJ[nanoIndex, drugIndex] != 0  # nano-drug connection

                    disease_adj = NN_ADJ[drug_adj[dd], disease] != 0
                    disease_adj = [d for d, b in zip(disease, disease_adj) if b]

                    if (len(disease_adj) > 0):
                        for di in range(len(disease_adj)):
                            diseaseIndex = disease_adj[di]
                            nano_disease = NN_ADJ[nanoIndex, diseaseIndex] != 0  # nano-disease connection
                            drug_disease = NN_ADJ[drugIndex, diseaseIndex] != 0  # drug-disease connection

                            if (nano_drug & nano_disease & drug_disease):
                                cliques_index = (nanoIndex, drugIndex, diseaseIndex)
                                cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[diseaseIndex])
                                cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, diseaseIndex],
                                                 ADJ_sign[drugIndex, diseaseIndex])
                                known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, diseaseIndex],
                                                 ADJ_known[drugIndex, diseaseIndex])
                                if checkClique_one(queryInput, cliques_index):
                                    cliques_NDrDi.add(
                                        (cliques_index, cliques_names, cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE

                            chem_adj = NN_ADJ[disease_adj[di], chemical] != 0
                            chem_adj = [d for d, b in zip(chemical, chem_adj) if b]

                            if (len(chem_adj) > 0):
                                for cc in range(len(chem_adj)):
                                    chemicalIndex = chem_adj[cc]
                                    nano_chem = NN_ADJ[nanoIndex, chemicalIndex] != 0  # nano-chem connection
                                    drug_chemical = NN_ADJ[drugIndex, chemicalIndex] != 0  # drug-chem connection
                                    disease_chemical = NN_ADJ[
                                                           diseaseIndex, chemicalIndex] != 0  # chem-disease connection

                                    isClique = nano_drug & nano_disease & nano_chem & drug_disease & drug_chemical & disease_chemical
                                    if (isClique):
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
                                        if checkClique_one(queryInput, cliques_index):
                                            cliques_NDrDiC.add((cliques_index, cliques_names,
                                                                cliques_edges,known_edges))  # Clique NANO-DRUG-DISEASE-CHEMICAL

                                    if (nano_drug & nano_chem & drug_chemical):
                                        cliques_index = (nanoIndex, drugIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                        ADJ_sign[drugIndex, chemicalIndex])
                                        known_edges = (
                                        ADJ_known[nanoIndex, drugIndex],  ADJ_known[nanoIndex, chemicalIndex],
                                        ADJ_known[drugIndex, chemicalIndex])
                                        if checkClique_one(queryInput, cliques_index):
                                            cliques_NDrC.add((cliques_index, cliques_names,
                                                              cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL

                                    if (nano_disease & nano_chem & disease_chemical):
                                        cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                        cliques_edges = (
                                        ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                        ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (
                                        ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],
                                        ADJ_known[diseaseIndex, chemicalIndex])
                                        if checkClique_one(queryInput, cliques_index):
                                            cliques_NDiC.add((cliques_index, cliques_names,
                                                              cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL

                                    if (drug_disease & drug_chemical & disease_chemical):
                                        cliques_index = (drugIndex, diseaseIndex, chemicalIndex)
                                        cliques_names = (
                                        elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                        cliques_edges = (
                                        ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],
                                        ADJ_sign[diseaseIndex, chemicalIndex])
                                        known_edges = (
                                        ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],
                                        ADJ_known[diseaseIndex, chemicalIndex])
                                        if checkClique_one(queryInput, cliques_index):
                                            cliques_DrDiC.add((cliques_index, cliques_names,
                                                               cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL

                    else:  # nano, drugs but no disease
                        chem_adj = NN_ADJ[drug_adj[dd], chemical] != 0
                        chem_adj = [d for d, b in zip(chemical, chem_adj) if b]
                        if (len(chem_adj) > 0):
                            for cc in range(len(chem_adj)):
                                chemicalIndex = chem_adj[cc]
                                nano_chem = NN_ADJ[nanoIndex, chemicalIndex] != 0  # nano-chem connection
                                drug_chemical = NN_ADJ[drugIndex, chemicalIndex] != 0  # drug-chem connection
                                if (nano_drug & nano_chem & drug_chemical):
                                    cliques_index = (nanoIndex, drugIndex, chemicalIndex)
                                    cliques_names = (elemName[nanoIndex], elemName[drugIndex], elemName[chemicalIndex])
                                    cliques_edges = (ADJ_sign[nanoIndex, drugIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                                     ADJ_sign[drugIndex, chemicalIndex])
                                    known_edges = (ADJ_known[nanoIndex, drugIndex], ADJ_known[nanoIndex, chemicalIndex],
                                                     ADJ_known[drugIndex, chemicalIndex])
                                    if checkClique_one(queryInput, cliques_index):
                                        cliques_NDrC.add(
                                            (cliques_index, cliques_names, cliques_edges,known_edges))  # Clique NANO-DRUG-CHEMICAL
            else:  # nano but no drugs
                disease_adj = NN_ADJ[nanoIndex, disease] != 0
                disease_adj = [d for d, b in zip(disease, drug_adj) if b]
                if (len(disease_adj) > 0):
                    for di in range(len(disease_adj)):
                        diseaseIndex = disease_adj[di]
                        nano_disease = NN_ADJ[nanoIndex, diseaseIndex] != 0  # nano-disease connection
                        chem_adj = NN_ADJ[diseaseIndex, chemical] != 0
                        chem_adj = [d for d, b in zip(chemical, chem_adj) if b]
                        if (len(chem_adj) > 0):
                            for cc in range(len(chem_adj)):
                                chemicalIndex = chem_adj[cc]
                                nano_chem = NN_ADJ[nanoIndex, chemicalIndex] != 0  # nano-chem connection
                                disease_chemical = NN_ADJ[diseaseIndex.chemicalIndex] != 0  # drug-chem connection

                                if (nano_disease & nano_chem & disease_chemical):
                                    cliques_index = (nanoIndex, diseaseIndex, chemicalIndex)
                                    cliques_names = (
                                    elemName[nanoIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                    cliques_edges = (
                                    ADJ_sign[nanoIndex, diseaseIndex], ADJ_sign[nanoIndex, chemicalIndex],
                                    ADJ_sign[diseaseIndex, chemicalIndex])
                                    known_edges = (
                                    ADJ_known[nanoIndex, diseaseIndex], ADJ_known[nanoIndex, chemicalIndex],
                                    ADJ_known[diseaseIndex, chemicalIndex])
                                    if checkClique_one(queryInput, cliques_index):
                                        cliques_NDiC.add((cliques_index, cliques_names,
                                                          cliques_edges,known_edges))  # Clique NANO-DISEASE-CHEMICAL
    else:  # no nano in the submatrix
        if (len(drug) > 0):
            for dd in range(len(drug)):
                drugIndex = drug[dd]
                disease_adj = NN_ADJ_red[drugIndex, disease] != 0
                disease_adj = [d for d, b in zip(disease, disease_adj) if b]
                if (len(disease_adj) > 0):
                    for di in range(len(disease_adj)):
                        diseaseIndex = disease_adj[di]
                        drug_disease = NN_ADJ[drugIndex, diseaseIndex] != 0  # drug-disease connection
                        chem_adj = NN_ADJ[diseaseIndex, chemical] != 0
                        chem_adj = [d for d, b in zip(chemical, chem_adj) if b]
                        if (len(chem_adj) > 0):
                            for cc in range(len(chem_adj)):
                                chemicalIndex = chem_adj[cc]
                                drug_chemical = NN_ADJ[drugIndex, chemicalIndex] != 0  # nano-chem connection
                                disease_chemical = NN_ADJ[diseaseIndex, chemicalIndex] != 0  # drug-chem connection

                                if (drug_disease & drug_chemical & disease_chemical):
                                    cliques_index = (drugIndex, diseaseIndex, chemicalIndex)
                                    cliques_names = (
                                    elemName[drugIndex], elemName[diseaseIndex], elemName[chemicalIndex])
                                    cliques_edges = (
                                    ADJ_sign[drugIndex, diseaseIndex], ADJ_sign[drugIndex, chemicalIndex],
                                    ADJ_sign[diseaseIndex, chemicalIndex])
                                    known_edges = (
                                    ADJ_known[drugIndex, diseaseIndex], ADJ_known[drugIndex, chemicalIndex],
                                    ADJ_known[diseaseIndex, chemicalIndex])
                                    if checkClique_one(queryInput, cliques_index):
                                        cliques_DrDiC.add((cliques_index, cliques_names,
                                                           cliques_edges,known_edges))  # Clique DRUG-DISEASE-CHEMICAL

    Cliques = {'NanoDrugDiseaseChemical': list(cliques_NDrDiC), 'NanoDrugDisease': list(cliques_NDrDi),
               'NanoDrugChemical': list(cliques_NDrC), 'NanoDiseaseChemical': list(cliques_NDiC),
               'DrugDiseaseChemical': list(cliques_DrDiC)}

    return Cliques
