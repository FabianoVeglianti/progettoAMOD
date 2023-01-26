import numpy as np
import gurobipy as gb
from gurobipy import GRB
import pulp as p
import math
from math import floor
import time
from treelib import Node, Tree

def generateSubTree(tree, node, remainingLenght, listOfAvailableModules, nextIndex, cuttings, startModuleIndex, pruning, maxCuttingPatterns):
    """
    cuttings e' la lista del numero di moduli per ciascuna lunghezza ottenuta dal paper roll finora
    startModuleIndex e' l'indice del primo modulo da considerare per tagliare il paper roll
    nextIndex e' il prossimo indice del nodo dell'albero
    pruning e' un booleano che abilita/disabilita il pruning
    cuttingPatternsStartingWithModule e' una lista che in posizione i contiene il numero di cutting patterns che prevedono
        come primo cut la generazione del modulo i-esimo
    maxCuttingPatterns e'una lista che in posizione i contiene il numero massimo di cutting patterns che prevedono
        come primo cut la generazione del modulo i-esimo
    """
    for i in range(0, len(listOfAvailableModules)):
        if remainingLenght - listOfAvailableModules[i] >= 0:
            globalModuleIndex = startModuleIndex + i
            if(pruning and len(tree.leaves()) == maxCuttingPatterns):
                canICutMore = (remainingLenght - listOfAvailableModules[len(listOfAvailableModules) - 1] >= 0)
                if not canICutMore:
                    return nextIndex
            currentCuttings = cuttings.copy()
            currentCuttings[globalModuleIndex] = currentCuttings[globalModuleIndex] + 1
            newNode = tree.create_node(currentCuttings, nextIndex, parent=node)
            nextIndex = nextIndex + 1
            nextIndex = generateSubTree(tree, newNode, remainingLenght - listOfAvailableModules[i], listOfAvailableModules[i:], nextIndex, currentCuttings, globalModuleIndex, pruning, maxCuttingPatterns)

    return nextIndex

def determineInitialCuttingPatterns3(L, listOfModule, maxNumCuttingPatterns, debug):
    m = len(listOfModule)
    searchListOfModule = sorted(listOfModule, reverse=True)
    initialLenght = L
    A_R = []
    A_j = []

    remainingLenght = initialLenght
    indexOnModules = 0
    tree = Tree()
    cuttings = []


    M = maxNumCuttingPatterns
    X = m * (m + 1) / 2
    maxCuttingPatternsList = []
    for i in range(0, m):
        cuttings.append(0)
        maxCuttingPatternsList.append(floor(M * (m - i)/X))

    if(debug):

        print("Not Pruned")
        root = tree.create_node(cuttings, identifier=1)  # root node
        nextIndex = 2
        for i in range(0, m):
            subTree = Tree()
            currentCuttings = cuttings.copy()
            currentCuttings[i] = currentCuttings[i] + 1
            subTreeRoot = subTree.create_node(currentCuttings, nextIndex)

            nextIndex = nextIndex + 1
            print(initialLenght-searchListOfModule[i], searchListOfModule[i:], currentCuttings)
            nextIndex = generateSubTree(subTree, subTreeRoot, initialLenght - searchListOfModule[i], searchListOfModule[i:], nextIndex, currentCuttings, i, False, maxCuttingPatternsList[i])

            tree.paste(root.identifier, subTree)


        tree.show()

        print("\n\nPruned")
    prunedTree = Tree()
    prunedTreeRoot = prunedTree.create_node(cuttings, 1)

    nextIndex = 2
    for i in range(0, m):
        subTree = Tree()
        currentCuttings = cuttings.copy()
        currentCuttings[i] = currentCuttings[i] + 1
        subTreeRoot = subTree.create_node(currentCuttings, nextIndex)

        nextIndex = nextIndex + 1
        nextIndex = generateSubTree(subTree, subTreeRoot, initialLenght - searchListOfModule[i], searchListOfModule[i:],
                                    nextIndex, currentCuttings, i, True, maxCuttingPatternsList[i])
        prunedTree.paste(prunedTreeRoot.identifier, subTree)


    if(debug):
        prunedTree.show()
    leaves = prunedTree.leaves()

    for leaf in leaves:
        A_R.append(leaf._tag)

    return A_R





def determineInitialCuttingPatterns1(L, listOfModule):
    m = len(listOfModule)
    initialLenght = L
    A_R = []
    A_j = []
    for j in range(0, m):
        value = floor(L / listOfModule[j])
        for i in range(0, m):
            if i == j:
                A_j.append(value)
            else:
                A_j.append(0)
        A_R.append(A_j)
        A_j = []
    return A_R




def determineInitialCuttingPatterns2(L, listOfModule):
    m = len(listOfModule)
    A_R = []
    A_j = np.ndarray.tolist(np.zeros(m))

    for j in range(0, m):
        A_j[j] = floor(L / listOfModule[j])

        remainder = L - A_j[j] * listOfModule[j]

        if j != m-1:
            for k in range(j+1, m):
                A_j[k] = floor(remainder / listOfModule[k])
                remainder = remainder - A_j[k]

        A_R.append(A_j)
        A_j = np.ndarray.tolist(np.zeros(m))

    return A_R


def resolveSubproblem(listOfDemand, A_R):
    Y = []
    X = []

    #Creazione del modello
    primal = gb.Model("Primal")

    #Creazione delle variabili
    xVar = primal.addVars(len(A_R), vtype=GRB.CONTINUOUS, name ="x", lb=0.0)
    primal.update()

    #for i in range(len(cutScheme)):
    #    print(xVar[i])

    #Funzione obiettivo:
    primal.setObjective(xVar.sum(), GRB.MINIMIZE)

    #Vincoli del problema:

    npMatA_R = np.matrix(A_R).transpose()
   # print(npMatA_R)
   # print(npMatA_R[0,0], npMatA_R[0,1], npMatA_R[0,2], npMatA_R[0,3])
   #print(len(listOfDemand), len(cutScheme))
    demands = primal.addConstrs(sum(xVar[j] * npMatA_R[i,j] for j in range(len(A_R))) >= listOfDemand[i] for i in range(len(listOfDemand)))



    # Solver
    print("Problema")
    primal.update()
    primal.optimize()

    status = primal.getAttr("Status")
    if status == 3: #status = 3 means Infeasible Model
        print("Problema Infeasible")
        return primal, Y, X, status


  #  for v in primal.getVars():
   #     print(v.varName, v.x)

    # Stampa valore funzione obiettivo
    print('Valore ottimo della funzione obiettivo: ', primal.objVal)

    for v in primal.getVars():
        X.append(v.x)

    for constr in primal.getConstrs():
        Y.append(constr.Pi)

    print(primal.display())

    return primal, Y, X, status


def resolvePricing(L, listObjectiveFunction, listInequity):
    A_j = []

    pricing = gb.Model("Pricing")

    #Creazione delle variabili
    xVar = pricing.addVars(len(listObjectiveFunction), vtype=GRB.INTEGER, name = "x",lb=0.0)

    #Funzione obiettivo:
    pricing.setObjective(sum(xVar[j] * listObjectiveFunction[j] for j in range(len(listObjectiveFunction))), GRB.MAXIMIZE)

    #Vincoli del problema:
    demands = pricing.addConstr(sum(xVar[j] * listInequity[j] for j in range(len(listInequity))) <= L)


    pricing.update()
    pricing.optimize()



    #Stampa valore della funzione obiettivo
    print('Obj Pricing: ', pricing.objVal)

    #Verifico se il valore della funzione obiettivo e' maggiore di 1,
    #se cio' e' verificato, A_j diventerà il nuovo cutting pattern da considerare
    if pricing.objVal > 1:
        for v in pricing.getVars():
            A_j.append(v.x)

    return A_j, pricing.objVal


def updateA_R(A_R, A_j):
    A_R.append(A_j)
    return A_R

def roundUpSolution(X):
    objRoundedUp = 0
    for x_j in X:
        objRoundedUp += math.ceil(x_j)
    return objRoundedUp


if __name__ == '__main__':
    L = 100
    listOfModules = [20, 3, 1]
    maxNumCuttingPatterns = 6
    A_R = determineInitialCuttingPatterns3(L, listOfModules, maxNumCuttingPatterns, True)

    print(A_R)

    A_R = determineInitialCuttingPatterns2(L, listOfModules)
    print(A_R)