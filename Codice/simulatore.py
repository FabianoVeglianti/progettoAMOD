import json
import csv
import esecuzioneSingola as executer
from numpy import random
from numpy import linspace
from math import sqrt, floor, ceil
import numpy
from time import sleep

with open("paperRollLenght.json", "r") as infile:
    instances = json.load(infile)

print(instances)

def createInstanceAndRunSimulationDifferentPaperRollLenght(outputFilename, minPaperRollLenght, maxPaperRollLenght, paperRollLenghtStep):

    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["L", "mean_iterations", "std_iterations", "mean_elapsed_time", "std_elapsed_time", "mean_absolute_error", "std_absolute_error", "mean_relative_error", "std_relative_error"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        output = {}
        for L in range(minPaperRollLenght, maxPaperRollLenght, paperRollLenghtStep):
            output["L"] = L
            output["mean_iterations"] = 0.0
            output["std_iterations"] = 0.0
            output["mean_elapsed_time"] = 0.0
            output["std_elapsed_time"] = 0.0
            output["mean_absolute_error"] = 0.0
            output["std_absolute_error"] = 0.0
            output["mean_relative_error"] = 0.0
            output["std_relative_error"] = 0.0
            validInstances = 0.0
            random.seed(1)
            infeasible = 3
            numIterations = 0.0
            while(validInstances < 20.0):
                numModules = 20
                if(infeasible == 3 and numIterations >= 20.0 and validInstances < 10.0):
                    break
                numIterations += 1.0
                meanModules = 100
                halfDeltaModules = 50
                lowModules = meanModules - halfDeltaModules
                highModules = meanModules + halfDeltaModules
                modules = numpy.random.choice(lowModules + numpy.arange(2*halfDeltaModules+1), size=numModules, replace=False)

                meanDemands = 500
                halfDeltaDemands = 200
                lowDemands = meanDemands - halfDeltaDemands
                highDemands = meanDemands + halfDeltaDemands
                demands = numpy.random.choice(lowDemands + numpy.arange(2*halfDeltaDemands+1), size=numModules, replace=True)

                obj = executer.computeSolution(L, modules, demands)
                infeasible = obj[7]
                if obj[7] != 3 and obj[5] != 500:
                    validInstances += 1.0
                    output["std_iterations"] = output["std_iterations"] + (validInstances - 1.0) / validInstances * (obj[5] - output["mean_iterations"]) * (obj[5] - output["mean_iterations"])
                    output["mean_iterations"] = output["mean_iterations"] + 1.0/validInstances*(obj[5] - output["mean_iterations"])

                    output["std_elapsed_time"] = output["std_elapsed_time"] + (validInstances - 1.0) / validInstances * (obj[6] - output["mean_elapsed_time"]) * (obj[6] - output["mean_elapsed_time"])
                    output["mean_elapsed_time"] = output["mean_elapsed_time"] + 1.0 / validInstances * (obj[6] - output["mean_elapsed_time"])

                    output["std_absolute_error"] = output["std_absolute_error"] + (validInstances - 1.0) / validInstances * (obj[3] - output["mean_absolute_error"]) * (obj[3] - output["mean_absolute_error"])
                    output["mean_absolute_error"] = output["mean_absolute_error"] + 1.0 / validInstances * (obj[3] - output["mean_absolute_error"])

                    output["std_relative_error"] = output["std_relative_error"] + (validInstances - 1.0) / validInstances * (obj[4] - output["mean_relative_error"]) * (obj[4] - output["mean_relative_error"])
                    output["mean_relative_error"] = output["mean_relative_error"] + 1.0 / validInstances * (obj[4] - output["mean_relative_error"])


            if validInstances != 0:
                output["std_iterations"] = sqrt(output["std_iterations"] / validInstances)
                output["std_elapsed_time"] = sqrt(output["std_elapsed_time"] / validInstances)
                output["std_absolute_error"] = sqrt(output["std_absolute_error"] / validInstances)
                output["std_relative_error"] = sqrt(output["std_relative_error"] / validInstances)
            writer.writerow(output)

fileDebug = open("filedebug.txt", "w")
fileDebug.write("different paper roll lenght\n")
fileDebug.flush()
fileDebug.close()

#createInstanceAndRunSimulationDifferentPaperRollLenght("paperRollLenghtTest.csv", 100, 3000, 100)

def runSimulationDifferentPaperRollLenght(inputFilename, outputFilename):
    with open(inputFilename, "r") as infile:
        instances = json.load(infile)

    for instance in instances:
        print(instance)


    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["L", "obj_value_with_round_up", "obj_value", "absolute_error", "relative_error", "iterations", "elapsed_time","is_feasible"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for instance in instances:
            L = instance["L"]
            numModules = instance["numModules"]
            modules = instance["modules"]
            demands = instance["demands"]
            isValid = instance["isValid"]

            obj = executer.computeSolution(L, modules, demands)

     

            output = {}
            output["L"] = L
            output["obj_value_with_round_up"] = obj[1]
            output["obj_value"] = obj[2]
            output["absolute_error"] = obj[3]
            output["relative_error"] = obj[4]
            output["iterations"] = obj[5]
            output["elapsed_time"] = obj[6]
            if obj[7] == 3:
                output["is_feasible"] = "no"
            else:
                output["is_feasible"] = "yes"
            writer.writerow(output)




#runSimulationDifferentPaperRollLenght("paperRollLenght.json", "paperRollLenght.csv")

def createInstanceAndRunSimulationDifferentNumberOfModules(outputFilename, minNumModules, maxNumModules, numModulesStep):

    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["number_of_modules", "mean_iterations", "std_iterations", "mean_elapsed_time", "std_elapsed_time", "mean_absolute_error", "std_absolute_error", "mean_relative_error", "std_relative_error"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        output = {}
        for numModules in range(minNumModules, maxNumModules, numModulesStep):
            output["number_of_modules"] = numModules
            output["mean_iterations"] = 0.0
            output["std_iterations"] = 0.0
            output["mean_elapsed_time"] = 0.0
            output["std_elapsed_time"] = 0.0
            output["mean_absolute_error"] = 0.0
            output["std_absolute_error"] = 0.0
            output["mean_relative_error"] = 0.0
            output["std_relative_error"] = 0.0
            validInstances = 0.0
            random.seed(1)
            while(validInstances < 20.0):
                L = 1000
                meanModules = 100
                halfDeltaModules = 50
                lowModules = meanModules - halfDeltaModules
                highModules = meanModules + halfDeltaModules
                modules = numpy.random.choice(lowModules + numpy.arange(2*halfDeltaModules+1), size=numModules, replace=False)

                meanDemands = 500
                halfDeltaDemands = 200
                lowDemands = meanDemands - halfDeltaDemands
                highDemands = meanDemands + halfDeltaDemands
                demands = numpy.random.choice(lowDemands + numpy.arange(2*halfDeltaDemands+1), size=numModules, replace=True)

                obj = executer.computeSolution(L, modules, demands)

                if obj[7] != 3 and obj[5] != 500:
                    validInstances += 1.0
                    output["std_iterations"] = output["std_iterations"] + (validInstances - 1.0) / validInstances * (obj[5] - output["mean_iterations"]) * (obj[5] - output["mean_iterations"])
                    output["mean_iterations"] = output["mean_iterations"] + 1.0/validInstances*(obj[5] - output["mean_iterations"])

                    output["std_elapsed_time"] = output["std_elapsed_time"] + (validInstances - 1.0) / validInstances * (obj[6] - output["mean_elapsed_time"]) * (obj[6] - output["mean_elapsed_time"])
                    output["mean_elapsed_time"] = output["mean_elapsed_time"] + 1.0 / validInstances * (obj[6] - output["mean_elapsed_time"])

                    output["std_absolute_error"] = output["std_absolute_error"] + (
                                validInstances - 1.0) / validInstances * (obj[3] - output["mean_absolute_error"]) * (
                                                               obj[3] - output["mean_absolute_error"])
                    output["mean_absolute_error"] = output["mean_absolute_error"] + 1.0 / validInstances * (
                                obj[3] - output["mean_absolute_error"])

                    output["std_relative_error"] = output["std_relative_error"] + (
                                validInstances - 1.0) / validInstances * (obj[4] - output["mean_relative_error"]) * (
                                                               obj[4] - output["mean_relative_error"])
                    output["mean_relative_error"] = output["mean_relative_error"] + 1.0 / validInstances * (
                                obj[4] - output["mean_relative_error"])

            if validInstances != 0:
                output["std_iterations"] = sqrt(output["std_iterations"] / validInstances)
                output["std_elapsed_time"] = sqrt(output["std_elapsed_time"] / validInstances)
                output["std_absolute_error"] = sqrt(output["std_absolute_error"] / validInstances)
                output["std_relative_error"] = sqrt(output["std_relative_error"] / validInstances)
            writer.writerow(output)

fileDebug = open("filedebug.txt", "a")
fileDebug.write("different number of modules\n")
fileDebug.flush()
fileDebug.close()
#createInstanceAndRunSimulationDifferentNumberOfModules("numberOfModulesTest.csv", minNumModules = 5,maxNumModules = 85, numModulesStep = 5)

def runSimulationDifferentNumberOfModules(inputFilename, outputFilename):
    with open(inputFilename, "r") as infile:
        instances = json.load(infile)

    for instance in instances:
        print(instance)

    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["number_of_modules", "obj_value_with_round_up", "obj_value", "absolute_error", "relative_error", "iterations",
                      "elapsed_time", "is_feasible"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for instance in instances:
            L = instance["L"]
            numModules = instance["numModules"]
            modules = instance["modules"]
            demands = instance["demands"]
            isValid = instance["isValid"]

            obj = executer.computeSolution(L, modules, demands)

            output = {}
            output["number_of_modules"] = numModules
            output["obj_value_with_round_up"] = obj[1]
            output["obj_value"] = obj[2]
            output["absolute_error"] = obj[3]
            output["relative_error"] = obj[4]
            output["iterations"] = obj[5]
            output["elapsed_time"] = obj[6]
            if obj[7] == 3:
                output["is_feasible"] = "no"
            else:
                output["is_feasible"] = "yes"
            writer.writerow(output)

#runSimulationDifferentNumberOfModules("numberOfModules.json", "numberOfModules.csv")

def createInstanceAndRunSimulationDifferentMeanDemands(outputFilename, minNumMeanDemands, maxNumMeanDemands, numMeanDemandsStep):

    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["mean_demands", "mean_iterations", "std_iterations", "mean_elapsed_time", "std_elapsed_time", "mean_absolute_error", "std_absolute_error", "mean_relative_error", "std_relative_error"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        output = {}
        for meanDemands in range(minNumMeanDemands, maxNumMeanDemands, numMeanDemandsStep):


            output["mean_demands"] = meanDemands
            output["mean_iterations"] = 0.0
            output["std_iterations"] = 0.0
            output["mean_elapsed_time"] = 0.0
            output["std_elapsed_time"] = 0.0
            output["mean_absolute_error"] = 0.0
            output["std_absolute_error"] = 0.0
            output["mean_relative_error"] = 0.0
            output["std_relative_error"] = 0.0
            validInstances = 0.0
            random.seed(1)
            while(validInstances < 20.0):
                L = 1000
                numModules = 20

                meanModules = 100
                halfDeltaModules = 50
                lowModules = meanModules - halfDeltaModules
                highModules = meanModules + halfDeltaModules
                modules = numpy.random.choice(lowModules + numpy.arange(2*halfDeltaModules+1), size=numModules, replace=False)

               # meanDemands = 500
                halfDeltaDemands = 200
                lowDemands = meanDemands - halfDeltaDemands
                highDemands = meanDemands + halfDeltaDemands
                demands = numpy.random.choice(lowDemands + numpy.arange(2*halfDeltaDemands+1), size=numModules, replace=True)

                obj = executer.computeSolution(L, modules, demands)

                if obj[7] != 3 and obj[5] != 500:
                    validInstances += 1.0
                    output["std_iterations"] = output["std_iterations"] + (validInstances - 1.0) / validInstances * (obj[5] - output["mean_iterations"]) * (obj[5] - output["mean_iterations"])
                    output["mean_iterations"] = output["mean_iterations"] + 1.0/validInstances*(obj[5] - output["mean_iterations"])

                    output["std_elapsed_time"] = output["std_elapsed_time"] + (validInstances - 1.0) / validInstances * (obj[6] - output["mean_elapsed_time"]) * (obj[6] - output["mean_elapsed_time"])
                    output["mean_elapsed_time"] = output["mean_elapsed_time"] + 1.0 / validInstances * (obj[6] - output["mean_elapsed_time"])

                    output["std_absolute_error"] = output["std_absolute_error"] + (
                                validInstances - 1.0) / validInstances * (obj[3] - output["mean_absolute_error"]) * (
                                                               obj[3] - output["mean_absolute_error"])
                    output["mean_absolute_error"] = output["mean_absolute_error"] + 1.0 / validInstances * (
                                obj[3] - output["mean_absolute_error"])

                    output["std_relative_error"] = output["std_relative_error"] + (
                                validInstances - 1.0) / validInstances * (obj[4] - output["mean_relative_error"]) * (
                                                               obj[4] - output["mean_relative_error"])
                    output["mean_relative_error"] = output["mean_relative_error"] + 1.0 / validInstances * (
                                obj[4] - output["mean_relative_error"])

            if validInstances != 0:
                output["std_iterations"] = sqrt(output["std_iterations"] / validInstances)
                output["std_elapsed_time"] = sqrt(output["std_elapsed_time"] / validInstances)
                output["std_absolute_error"] = sqrt(output["std_absolute_error"] / validInstances)
                output["std_relative_error"] = sqrt(output["std_relative_error"] / validInstances)
            writer.writerow(output)

fileDebug = open("filedebug.txt", "a")
fileDebug.write("different demand\n")
fileDebug.flush()
fileDebug.close()
#createInstanceAndRunSimulationDifferentMeanDemands("meanDemandsTest.csv", minNumMeanDemands = 50, maxNumMeanDemands = 2050, numMeanDemandsStep = 50)

def runSimulationDifferentNumberOfMeanDemands(inputFilename, outputFilename):
    with open(inputFilename, "r") as infile:
        instances = json.load(infile)

    for instance in instances:
        print(instance)

    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["number_of_mean_demands", "demand_range", "obj_value_with_round_up", "obj_value", "absolute_error", "relative_error", "iterations",
                      "elapsed_time", "is_feasible"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for instance in instances:
            L = instance["L"]
            numModules = instance["numModules"]
            modules = instance["modules"]
            demands = instance["demands"]
            isValid = instance["isValid"]

            obj = executer.computeSolution(L, modules, demands)

            output = {}

            output["number_of_mean_demands"] = instance["meanDemand"]
            output["demand_range"] = instance["demandRange"]
            output["obj_value_with_round_up"] = obj[1]
            output["obj_value"] = obj[2]
            output["absolute_error"] = obj[3]
            output["relative_error"] = obj[4]
            output["iterations"] = obj[5]
            output["elapsed_time"] = obj[6]
            if obj[7] == 3:
                output["is_feasible"] = "no"
            else:
                output["is_feasible"] = "yes"
            writer.writerow(output)

#runSimulationDifferentNumberOfMeanDemands("meanDemands.json", "meanDemands.csv")

def createInstanceAndRunSimulationDifferentModuleLenghtSTD(outputFilename, minModuleLenghtstd, maxModuleLenghtstd, moduleLenghtstdStep):
    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["module_lenght_std", "mean_iterations", "std_iterations", "mean_elapsed_time", "std_elapsed_time", "mean_absolute_error", "std_absolute_error", "mean_relative_error", "std_relative_error"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        output = {}
        for stdModules in range(minModuleLenghtstd, maxModuleLenghtstd, moduleLenghtstdStep):

            output["module_lenght_std"] = stdModules
            output["mean_iterations"] = 0.0
            output["std_iterations"] = 0.0
            output["mean_elapsed_time"] = 0.0
            output["std_elapsed_time"] = 0.0
            output["mean_absolute_error"] = 0.0
            output["std_absolute_error"] = 0.0
            output["mean_relative_error"] = 0.0
            output["std_relative_error"] = 0.0
            validInstances = 0.0
            random.seed(1)
            while(validInstances < 20.0):
                L = 1000
                numModules = 20

                meanModules = 100
               # stdModules = 100 / 3
                variance = stdModules * stdModules
                lowModules = floor(meanModules - sqrt(12*variance+1)/2 + 0.5) # lower bound module lenght
                highModules = ceil(meanModules -0.5 + sqrt(12*variance+1)/2)  # upper bound module lenght


                halfDeltaModules = ceil((highModules - lowModules) / 2)

                modules = numpy.random.choice(lowModules + numpy.arange(2 * halfDeltaModules + 1), size=numModules,
                                              replace=False)


                meanDemands = 500
                halfDeltaDemands = 200
                lowDemands = meanDemands - halfDeltaDemands
                highDemands = meanDemands + halfDeltaDemands
                demands = numpy.random.choice(lowDemands + numpy.arange(2 * halfDeltaDemands + 1), size=numModules,
                                              replace=True)

                obj = executer.computeSolution(L, modules, demands)

                if obj[7] != 3 and obj[5] != 500:
                    validInstances += 1.0
                    output["std_iterations"] = output["std_iterations"] + (validInstances - 1.0) / validInstances * (
                                obj[5] - output["mean_iterations"]) * (obj[5] - output["mean_iterations"])
                    output["mean_iterations"] = output["mean_iterations"] + 1.0 / validInstances * (
                                obj[5] - output["mean_iterations"])

                    output["std_elapsed_time"] = output["std_elapsed_time"] + (
                                validInstances - 1.0) / validInstances * (obj[6] - output["mean_elapsed_time"]) * (
                                                             obj[6] - output["mean_elapsed_time"])
                    output["mean_elapsed_time"] = output["mean_elapsed_time"] + 1.0 / validInstances * (
                                obj[6] - output["mean_elapsed_time"])

                    output["std_absolute_error"] = output["std_absolute_error"] + (
                                validInstances - 1.0) / validInstances * (obj[3] - output["mean_absolute_error"]) * (
                                                               obj[3] - output["mean_absolute_error"])
                    output["mean_absolute_error"] = output["mean_absolute_error"] + 1.0 / validInstances * (
                                obj[3] - output["mean_absolute_error"])

                    output["std_relative_error"] = output["std_relative_error"] + (
                                validInstances - 1.0) / validInstances * (obj[4] - output["mean_relative_error"]) * (
                                                               obj[4] - output["mean_relative_error"])
                    output["mean_relative_error"] = output["mean_relative_error"] + 1.0 / validInstances * (
                                obj[4] - output["mean_relative_error"])

            if validInstances != 0:
                output["std_iterations"] = sqrt(output["std_iterations"] / validInstances)
                output["std_elapsed_time"] = sqrt(output["std_elapsed_time"] / validInstances)
                output["std_absolute_error"] = sqrt(output["std_absolute_error"] / validInstances)
                output["std_relative_error"] = sqrt(output["std_relative_error"] / validInstances)
            writer.writerow(output)


fileDebug = open("filedebug.txt", "a")
fileDebug.write("different module lenght std\n")
fileDebug.flush()
fileDebug.close()
#createInstanceAndRunSimulationDifferentModuleLenghtSTD("stdModulesLenghtTest.csv", 10, 60, 5)

def runSimulationDifferentModuleLenghtSTD(inputFilename, outputFilename):
    with open(inputFilename, "r") as infile:
        instances = json.load(infile)

    for instance in instances:
        print(instance)

    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["module_lenght_std", "obj_value_with_round_up", "obj_value", "absolute_error", "relative_error", "iterations",
                      "elapsed_time", "is_feasible"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for instance in instances:
            L = instance["L"]
            modules = instance["modules"]
            demands = instance["demands"]
            isValid = instance["isValid"]

            obj = executer.computeSolution(L, modules, demands)

            output = {}

            output["module_lenght_std"] = instance["stdModules"]
            output["obj_value_with_round_up"] = obj[1]
            output["obj_value"] = obj[2]
            output["absolute_error"] = obj[3]
            output["relative_error"] = obj[4]
            output["iterations"] = obj[5]
            output["elapsed_time"] = obj[6]
            if obj[7] == 3:
                output["is_feasible"] = "no"
            else:
                output["is_feasible"] = "yes"
            writer.writerow(output)

#runSimulationDifferentModuleLenghtSTD("stdModulesLenght.json", "stdModulesLenght.csv")

def createInstanceAndRunSimulationDifferentModuleLenghtMean(outputFilename, minModuleLenghtMean, maxModuleLenghtMean, moduleLenghtMeanStep):
    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["module_lenght_mean", "mean_iterations", "std_iterations", "mean_elapsed_time", "std_elapsed_time", "mean_absolute_error", "std_absolute_error", "mean_relative_error", "std_relative_error"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        output = {}
        for meanModules in range(minModuleLenghtMean, maxModuleLenghtMean, moduleLenghtMeanStep):

            output["module_lenght_mean"] = meanModules
            output["mean_iterations"] = 0.0
            output["std_iterations"] = 0.0
            output["mean_elapsed_time"] = 0.0
            output["std_elapsed_time"] = 0.0
            output["mean_absolute_error"] = 0.0
            output["std_absolute_error"] = 0.0
            output["mean_relative_error"] = 0.0
            output["std_relative_error"] = 0.0
            validInstances = 0.0
            random.seed(1)
            while(validInstances < 20.0):
                L = 1000
                numModules = 20

              #  meanModules = 100
                halfDeltaModules = 50
                lowModules = meanModules - halfDeltaModules
                highModules = meanModules + halfDeltaModules
                modules = numpy.random.choice(lowModules + numpy.arange(2*halfDeltaModules+1), size=numModules, replace=False)
                print("modules:", modules)
                meanDemands = 500
                halfDeltaDemands = 200
                lowDemands = meanDemands - halfDeltaDemands
                highDemands = meanDemands + halfDeltaDemands
                demands = numpy.random.choice(lowDemands + numpy.arange(2*halfDeltaDemands+1), size=numModules, replace=True)

                obj = executer.computeSolution(L, modules, demands)

                if obj[7] != 3 and obj[5] != 500:
                    validInstances += 1.0
                    output["std_iterations"] = output["std_iterations"] + (validInstances - 1.0) / validInstances * (
                            obj[5] - output["mean_iterations"]) * (obj[5] - output["mean_iterations"])
                    output["mean_iterations"] = output["mean_iterations"] + 1.0 / validInstances * (
                            obj[5] - output["mean_iterations"])

                    output["std_elapsed_time"] = output["std_elapsed_time"] + (
                            validInstances - 1.0) / validInstances * (obj[6] - output["mean_elapsed_time"]) * (
                                                         obj[6] - output["mean_elapsed_time"])
                    output["mean_elapsed_time"] = output["mean_elapsed_time"] + 1.0 / validInstances * (
                            obj[6] - output["mean_elapsed_time"])

                    output["std_absolute_error"] = output["std_absolute_error"] + (
                                validInstances - 1.0) / validInstances * (obj[3] - output["mean_absolute_error"]) * (
                                                               obj[3] - output["mean_absolute_error"])
                    output["mean_absolute_error"] = output["mean_absolute_error"] + 1.0 / validInstances * (
                                obj[3] - output["mean_absolute_error"])

                    output["std_relative_error"] = output["std_relative_error"] + (
                                validInstances - 1.0) / validInstances * (obj[4] - output["mean_relative_error"]) * (
                                                               obj[4] - output["mean_relative_error"])
                    output["mean_relative_error"] = output["mean_relative_error"] + 1.0 / validInstances * (
                                obj[4] - output["mean_relative_error"])
                #    print(validInstances)
                #   sleep(10)

            if validInstances != 0:
                output["std_iterations"] = sqrt(output["std_iterations"] / validInstances)
                output["std_elapsed_time"] = sqrt(output["std_elapsed_time"] / validInstances)
                output["std_absolute_error"] = sqrt(output["std_absolute_error"] / validInstances)
                output["std_relative_error"] = sqrt(output["std_relative_error"] / validInstances)
            writer.writerow(output)


fileDebug = open("filedebug.txt", "a")
fileDebug.write("different module lenght mean\n")
fileDebug.flush()
fileDebug.close()
# 50 575 25
#createInstanceAndRunSimulationDifferentModuleLenghtMean("prova.csv", minModuleLenghtMean = 400, maxModuleLenghtMean = 425, moduleLenghtMeanStep = 25)

def runSimulationDifferentModuleLenghtMean(inputFilename, outputFilename):
    with open(inputFilename, "r") as infile:
        instances = json.load(infile)

    for instance in instances:
        print(instance)

    with open(outputFilename, mode='w') as csv_file:
        fieldnames = ["module_lenght_mean", "obj_value_with_round_up", "obj_value", "absolute_error", "relative_error", "iterations",
                      "elapsed_time", "is_feasible"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for instance in instances:
            L = instance["L"]
            modules = instance["modules"]
            demands = instance["demands"]
            isValid = instance["isValid"]

            obj = executer.computeSolution(L, modules, demands)

            output = {}

            output["module_lenght_mean"] = instance["meanModules"]
            output["obj_value_with_round_up"] = obj[1]
            output["obj_value"] = obj[2]
            output["absolute_error"] = obj[3]
            output["relative_error"] = obj[4]
            output["iterations"] = obj[5]
            output["elapsed_time"] = obj[6]
            if obj[7] == 3:
                output["is_feasible"] = "no"
            else:
                output["is_feasible"] = "yes"
            writer.writerow(output)

#runSimulationDifferentModuleLenghtSTD("meanModuleLenght.json", "meanModuleLenght.csv")