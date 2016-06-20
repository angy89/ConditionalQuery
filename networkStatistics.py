import random
import numpy as np
import sys
from collections import namedtuple

Edge = namedtuple('Edge', ['id','count', 'source', 'type', 'target', 'color', 'weight','isKnown'])
Node = namedtuple('Node', ['id', 'label', 'fixedSize', 'color', 'type', 'x', 'y', 'size'])


def networkStatistics(CS, ADJ_sign, ADJ_known,indicesBool, elemName):
    NDrDiC = list(CS['NanoDrugDiseaseChemical'])
    NDrDi = list(CS['NanoDrugDisease'])
    NDrC = list(CS['NanoDrugChemical'])
    NDiC = list(CS['NanoDiseaseChemical'])
    DrDiC = list(CS['DrugDiseaseChemical'])

    eIdx = 1
    knownCount = 0
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
        res = NDrDiC_Net(NDrDiC[i][0][0], NDrDiC[i][0][1], NDrDiC[i][0][2], NDrDiC[i][0][3], ADJ_sign, ADJ_known, eIdx, Net)
        Net = res['Net']
        eIdx = res['eIdx']
        knownCount += res['knownCount']
        edges.update(res['edges'])

    for i in range(len(NDrDi)):
        res = NDrDi_Net(NDrDi[i][0][0], NDrDi[i][0][1], NDrDi[i][0][2], ADJ_sign, ADJ_known, eIdx, Net)
        Net = res['Net']
        eIdx = res['eIdx']
        knownCount += res['knownCount']
        edges.update(res['edges'])

    for i in range(len(NDrC)):
        res = NDrC_Net(NDrC[i][0][0], NDrC[i][0][1], NDrC[i][0][2], ADJ_sign, ADJ_known, eIdx, Net)
        Net = res['Net']
        eIdx = res['eIdx']
        knownCount += res['knownCount']
        edges.update(res['edges'])

    for i in range(len(NDiC)):
        res = NDiC_Net(NDiC[i][0][0], NDiC[i][0][1], NDiC[i][0][2], ADJ_sign, ADJ_known, eIdx, Net)
        Net = res['Net']
        eIdx = res['eIdx']
        knownCount += res['knownCount']
        edges.update(res['edges'])

    for i in range(len(DrDiC)):
        res = DrDiC_Net(DrDiC[i][0][0], DrDiC[i][0][1], DrDiC[i][0][2], ADJ_sign, ADJ_known, eIdx, Net)
        Net = res['Net']
        eIdx = res['eIdx']
        knownCount += res['knownCount']
        edges.update(res['edges'])

    nodes = set()
    for i in range(len(nodesID)):
        nodes.update(generateNode(nodesID[i], indicesBool, Net, elemName))

    nodesDict = []
    for n in nodes:
        nodesDict.append(n._asdict())
    edgesDict = []
    for e in edges:
        edgesDict.append(e._asdict())

    return {'nodes': nodesDict, 'edges': edgesDict, 'knownCount': knownCount}


def generateNode(nodeId, indicesBool, Net, elemName):
    node_color = {}
    node_color['nano'] = '#ff0000'
    node_color['drug'] = '#0000ff'
    node_color['chemical'] = '#00ff00'
    node_color['disease'] = '#ff00ff'

    # nodePos = nodesID.index(nodeID)
    nodeDegree = np.sum(Net[nodeId, :] != 0)
    node = []

    if indicesBool['nano'][nodeId]:
        node.append(Node(id=nodeId, label=elemName[nodeId], fixedSize=1, color=node_color['nano'], type='nano',
                         x=random.randint(0, 1000), y=random.randint(0, 1000), size=nodeDegree))

    if indicesBool['drug'][nodeId]:
        node.append(Node(id=nodeId, label=elemName[nodeId], fixedSize=1, color=node_color['drug'], type='drug',
                         x=random.randint(0, 1000), y=random.randint(0, 1000), size=nodeDegree))

    if indicesBool['disease'][nodeId]:
        node.append(Node(id=nodeId, label=elemName[nodeId], fixedSize=1, color=node_color['disease'], type='disease',
                         x=random.randint(0, 1000), y=random.randint(0, 1000), size=nodeDegree))

    if indicesBool['chemical'][nodeId]:
        node.append(Node(id=nodeId, label=elemName[nodeId], fixedSize=1, color=node_color['chemical'], type='chemical',
                         x=random.randint(0, 1000), y=random.randint(0, 1000), size=nodeDegree))

    return node


def NDrDiC_Net(nanoIndex, drugIndex, diseaseIndex, chemicalIndex, ADJ_sign, ADJ_known,eIdx, Net):
    pEdgeCol = '#ff9999'
    nEdgeCol = '#99ff99'

    edges = []
    knownCount = 0
    
    Net[nanoIndex, drugIndex] = ADJ_sign[nanoIndex, drugIndex]
    Net[drugIndex, nanoIndex] = ADJ_sign[nanoIndex, drugIndex]

    Net[nanoIndex, diseaseIndex] = ADJ_sign[nanoIndex, diseaseIndex]
    Net[diseaseIndex, nanoIndex] = ADJ_sign[nanoIndex, diseaseIndex]

    Net[nanoIndex, chemicalIndex] = ADJ_sign[nanoIndex, chemicalIndex]
    Net[chemicalIndex, nanoIndex] = ADJ_sign[nanoIndex, chemicalIndex]

    Net[drugIndex, diseaseIndex] = ADJ_sign[drugIndex, diseaseIndex]
    Net[diseaseIndex, drugIndex] = ADJ_sign[drugIndex, diseaseIndex]

    Net[drugIndex, chemicalIndex] = ADJ_sign[drugIndex, chemicalIndex]
    Net[chemicalIndex, drugIndex] = ADJ_sign[drugIndex, chemicalIndex]

    Net[diseaseIndex, chemicalIndex] = ADJ_sign[diseaseIndex, chemicalIndex]
    Net[chemicalIndex, diseaseIndex] = ADJ_sign[diseaseIndex, chemicalIndex]

    if ADJ_known[nanoIndex,drugIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=drugIndex, color='Blue', weight=ADJ_sign[nanoIndex, drugIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=drugIndex,color=pEdgeCol if ADJ_sign[nanoIndex, drugIndex] > 0 else nEdgeCol, weight=ADJ_sign[nanoIndex, drugIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=drugIndex,color=pEdgeCol if ADJ_sign[nanoIndex, drugIndex] > 0 else nEdgeCol, weight=ADJ_sign[nanoIndex, drugIndex],isKnown=0))
    eIdx += 1
    
    if ADJ_known[nanoIndex, diseaseIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=diseaseIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=0))

    eIdx += 1
    
    if ADJ_known[nanoIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=0))

    eIdx += 1
    
    if ADJ_known[drugIndex, diseaseIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=drugIndex, type='curve', target=diseaseIndex,
                          color='Blue', weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=0))
    
    eIdx += 1

    if ADJ_known[drugIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=drugIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=1))

    else:
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    if ADJ_known[diseaseIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=diseaseIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=diseaseIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[diseaseIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=1))

    else:
        edges.append(Edge(id=eIdx, count = 0, source=diseaseIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[diseaseIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    # return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
    return {'edges': edges, 'eIdx': eIdx, 'Net': Net, 'knownCount': knownCount}


def NDrDi_Net(nanoIndex, drugIndex, diseaseIndex, ADJ_sign,ADJ_known, eIdx, Net):
    pEdgeCol = '#ff9999'
    nEdgeCol = '#99ff99'

    edges = []
    knownCount = 0

    Net[nanoIndex, drugIndex] = ADJ_sign[nanoIndex, drugIndex]
    Net[drugIndex, nanoIndex] = ADJ_sign[nanoIndex, drugIndex]

    Net[nanoIndex, diseaseIndex] = ADJ_sign[nanoIndex, diseaseIndex]
    Net[diseaseIndex, nanoIndex] = ADJ_sign[nanoIndex, diseaseIndex]

    Net[drugIndex, diseaseIndex] = ADJ_sign[drugIndex, diseaseIndex]
    Net[diseaseIndex, drugIndex] = ADJ_sign[drugIndex, diseaseIndex]

    if ADJ_known[nanoIndex,drugIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=drugIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, drugIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=drugIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, drugIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, drugIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=drugIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, drugIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, drugIndex],isKnown=0))
    eIdx += 1
    
    if ADJ_known[nanoIndex, diseaseIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=diseaseIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=0))

    eIdx += 1
 
    if ADJ_known[drugIndex, diseaseIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=drugIndex, type='curve', target=diseaseIndex,
                          color='Blue', weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=0))
    
    eIdx += 1

    # return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
    return {'edges': edges, 'eIdx': eIdx, 'Net': Net, 'knownCount': knownCount}


def NDrC_Net(nanoIndex, drugIndex, chemicalIndex, ADJ_sign, ADJ_known, eIdx, Net):
    pEdgeCol = '#ff9999'
    nEdgeCol = '#99ff99'

    edges = []
    knownCount = 0

    Net[nanoIndex, drugIndex] = ADJ_sign[nanoIndex, drugIndex]
    Net[drugIndex, nanoIndex] = ADJ_sign[nanoIndex, drugIndex]

    Net[nanoIndex, chemicalIndex] = ADJ_sign[nanoIndex, chemicalIndex]
    Net[chemicalIndex, nanoIndex] = ADJ_sign[nanoIndex, chemicalIndex]

    Net[drugIndex, chemicalIndex] = ADJ_sign[drugIndex, chemicalIndex]
    Net[chemicalIndex, drugIndex] = ADJ_sign[drugIndex, chemicalIndex]

    if ADJ_known[nanoIndex,drugIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=drugIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, drugIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=drugIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, drugIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, drugIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=drugIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, drugIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, drugIndex],isKnown=0))
    eIdx += 1

    if ADJ_known[nanoIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    if ADJ_known[drugIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=drugIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=1))

    else:
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    # return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
    return {'edges': edges, 'eIdx': eIdx, 'Net': Net, 'knownCount': knownCount}


def NDiC_Net(nanoIndex, diseaseIndex, chemicalIndex, ADJ_sign, ADJ_known, eIdx, Net):
    pEdgeCol = '#ff9999'
    nEdgeCol = '#99ff99'

    edges = []
    knownCount = 0

    Net[nanoIndex, diseaseIndex] = ADJ_sign[nanoIndex, diseaseIndex]
    Net[diseaseIndex, nanoIndex] = ADJ_sign[nanoIndex, diseaseIndex]

    Net[nanoIndex, chemicalIndex] = ADJ_sign[nanoIndex, chemicalIndex]
    Net[chemicalIndex, nanoIndex] = ADJ_sign[nanoIndex, chemicalIndex]

    Net[diseaseIndex, chemicalIndex] = ADJ_sign[diseaseIndex, chemicalIndex]
    Net[chemicalIndex, diseaseIndex] = ADJ_sign[diseaseIndex, chemicalIndex]

    if ADJ_known[nanoIndex, diseaseIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=diseaseIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, diseaseIndex],isKnown=0))

    eIdx += 1
    
    if ADJ_known[nanoIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=nanoIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=nanoIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[nanoIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[nanoIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    if ADJ_known[diseaseIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=diseaseIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=diseaseIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[diseaseIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=diseaseIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[diseaseIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    # return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
    return {'edges': edges, 'eIdx': eIdx, 'Net': Net, 'knownCount': knownCount}


def DrDiC_Net(drugIndex, diseaseIndex, chemicalIndex, ADJ_sign, ADJ_known, eIdx, Net):
    pEdgeCol = '#ff9999'
    nEdgeCol = '#99ff99'

    edges = []
    knownCount = 0

    Net[drugIndex, diseaseIndex] = ADJ_sign[drugIndex, diseaseIndex]
    Net[diseaseIndex, drugIndex] = ADJ_sign[drugIndex, diseaseIndex]

    Net[drugIndex, chemicalIndex] = ADJ_sign[drugIndex, chemicalIndex]
    Net[chemicalIndex, drugIndex] = ADJ_sign[drugIndex, chemicalIndex]

    Net[diseaseIndex, chemicalIndex] = ADJ_sign[diseaseIndex, chemicalIndex]
    Net[chemicalIndex, diseaseIndex] = ADJ_sign[diseaseIndex, chemicalIndex]

    if ADJ_known[drugIndex, diseaseIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=drugIndex, type='curve', target=diseaseIndex,
                          color='Blue', weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=diseaseIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, diseaseIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, diseaseIndex],isKnown=0))
    
    eIdx += 1

    if ADJ_known[drugIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=drugIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=drugIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[drugIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[drugIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    if ADJ_known[diseaseIndex, chemicalIndex]==1:
        edges.append(Edge(id=eIdx, count = 1, source=diseaseIndex, type='curve', target=chemicalIndex,
                          color='Blue', weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=1))
        eIdx += 1
        knownCount += 1
        edges.append(Edge(id=eIdx, count = 0, source=diseaseIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[diseaseIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=1))
    else:
        edges.append(Edge(id=eIdx, count = 0, source=diseaseIndex, type='curve', target=chemicalIndex,
                      color=pEdgeCol if ADJ_sign[diseaseIndex, chemicalIndex] > 0 else nEdgeCol,
                      weight=ADJ_sign[diseaseIndex, chemicalIndex],isKnown=0))

    eIdx += 1

    # return {'nodes': nodes, 'edges':edges, 'eIdx':eIdx}
    return {'edges': edges, 'eIdx': eIdx, 'Net': Net, 'knownCount': knownCount}

