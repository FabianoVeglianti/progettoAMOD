import cuttingStock as cs
import numpy as np
from time import sleep
from time import time
import math

L = 25
listOfModules = [9,8,7,6]
listOfDemands = [354,872,334,221]

n = len(listOfModules)

def computeSolution(L, listOfModules, listOfDemands):
    m = len(listOfModules)
    print("Numero di moduli: ", m)
    maxNumInitialCuttingPatterns = 2 * m
    startTime = time()
    counter = 0

    #inizializzazione
    A_R = cs.determineInitialCuttingPatterns1(L, listOfModules)
  #  A_R = cs.determineInitialCuttingPatterns2(L, listOfModules)


    isOpt = False

    while (True):
        try:
            if isOpt:  #Controllo se ho ottenuto la soluzione ottima.
                objValRoundedUpSolution = cs.roundUpSolution(X)
                err_abs = objValRoundedUpSolution - D.objVal
                print(objValRoundedUpSolution)
              #  sleep(3)
                err_apx = (objValRoundedUpSolution - D.objVal) / objValRoundedUpSolution

                print("\n\nTrovata la soluzione ottima!\n")
                print(f"Valore soluzione corrente: {D.objVal}")
                for v in D.getVars():
                    print(v.varName, v.x)
                print(f"Valore della soluzione con round-up: {objValRoundedUpSolution}")
                for v in D.getVars():
                    print(v.varName, math.ceil(v.x))
                print(f"Valore dell'errore Assoluto: {err_abs}")
                print(f"Valore dell'errore Relativo: {err_apx}")
                endTime = time()
                return dualObj, objValRoundedUpSolution, D.objVal ,err_abs, err_apx, counter, (endTime - startTime), status
            else:
                counter += 1

                if counter == 300:
                    objValRoundedUpSolution = cs.roundUpSolution(X)
                    print(f"Valore soluzione corrente: {D.objVal}")
                    print(f"Valore della soluzione con round-up: {objValRoundedUpSolution}")
                    endTime = time()
                    return dualObj, objValRoundedUpSolution, D.objVal, 0, 0, counter, (endTime - startTime), status


                D, Y, X, status = cs.resolveSubproblem(listOfDemands, A_R)
                if status == 3:
                    return 0, 0, 0, 0, 0, 0, 0, status

                print(f"Y = {Y}")  ##Valori del problema DUALE
                print(f"X = {X}")  ##Valori del problema PRIMALE

                enteringPattern, dualObj = cs.resolvePricing(L, Y, listOfModules)
                print("entering pattern", enteringPattern)
                print("dual obj", dualObj)
                isOpt = (len(enteringPattern) == 0)
                if isOpt == False:
                    A_R = cs.updateA_R(A_R, enteringPattern)
                print("\nA_R", A_R)


        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                print("L'istanza non è corretta.")
                break
            else:
                print(err)
                break



if __name__ == '__main__':
    output = computeSolution(L, listOfModules, listOfDemands)
    print("Output")
    print(("%s \n" % str(output)))


