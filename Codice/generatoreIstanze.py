import json
from numpy import random
from numpy import linspace
"""

random.seed(1)

meanModules = 100
stdModules = 100/3


lowModules = 0
highModules = 200

L = 1000
numModules = 20

modules = []
while len(modules) < numModules:
    sample = round(random.normal(meanModules, stdModules))
    if sample > lowModules and sample <= highModules:
        modules.append(sample)

meanDemands = 500
stdDemands = 200/3

lowDemands = 300
highDemands = 700

demands = []
while len(demands) < numModules:
    sample = round(random.normal(meanDemands, stdDemands))
    if sample > lowDemands and sample <= highDemands:
        demands.append(sample)
print(L)
print(sorted(modules))
print(demands)
instance = {}
instance["L"] = L
instance["numModules"] = len(modules)
instance["modules"] = sorted(modules)
instance["demands"] = demands
instance["isValid"] = max(modules) < L
print(instance)
"""


def generateInstancesWithDifferentPaperRollLenght(outputFileName, minPaperRollLenght, maxPaperRollLenght, paperRollLenghtStep):
    random.seed(1)
    numModules = 20

    meanModules = 100
    stdModules = 100 / 3
    lowModules = 0      #lower bound module lenght
    highModules = 200   #upper bound module lenght
    modules = []
    while len(modules) < numModules:
        sample = round(random.normal(meanModules, stdModules))
        if sample > lowModules and sample <= highModules:
            modules.append(sample)


    meanDemands = 500
    stdDemands = 200 / 3
    lowDemands = 300
    highDemands = 700
    demands = []
    while len(demands) < numModules:
        sample = round(random.normal(meanDemands, stdDemands))
        if sample > lowDemands and sample <= highDemands:
            demands.append(sample)


    instances = []
    for L in range(minPaperRollLenght, maxPaperRollLenght, paperRollLenghtStep):
        instance = {}
        instance["L"] = L
        instance["numModules"] = len(modules)
        instance["modules"] = sorted(modules)
        instance["demands"] = demands
        instance["isValid"] = max(modules) < L
        instances.append(instance)

    with open(outputFileName, "w") as outfile:
        json.dump(instances, outfile)


def generateInstancesWithDifferentNumberOfModules(outputFileName, minNumModules, maxNumModules, numModulesStep):
    random.seed(1)
    L = 1000

    meanModules = 100   #mean module lenght
    stdModules = 100 / 3
    lowModules = 0      #lower bound module lenght
    highModules = 200   #upper bound module lenght

    meanDemands = 500
    stdDemands = 200 / 3
    lowDemands = 300
    highDemands = 700


    instances = []
    for numModules in range(minNumModules, maxNumModules, numModulesStep):

        modules = []
        while len(modules) < numModules:
            sample = round(random.normal(meanModules, stdModules))
            if sample > lowModules and sample <= highModules:
                modules.append(sample)

        demands = []
        while len(demands) < numModules:
            sample = round(random.normal(meanDemands, stdDemands))
            if sample > lowDemands and sample <= highDemands:
                demands.append(sample)
        instance = {}
        instance["L"] = L
        instance["numModules"] = len(modules)
        instance["modules"] = sorted(modules)
        instance["demands"] = demands
        instance["isValid"] = max(modules) < L
        instances.append(instance)

    with open(outputFileName, "w") as outfile:
        json.dump(instances, outfile)


def generateInstancesWithDifferentNumberOfMeanDemands(outputFileName, minNumMeanDemands, maxNumMeanDemands, numMeanDemandsStep):
    random.seed(1)
    L = 1000
    numModules = 20

    meanModules = 100
    stdModules = 100 / 3
    lowModules = 0      #lower bound module lenght
    highModules = 200   #upper bound module lenght
    modules = []
    while len(modules) < numModules:
        sample = round(random.normal(meanModules, stdModules))
        if sample > lowModules and sample <= highModules:
            modules.append(sample)


    instances = []
    for meanDemands in range(minNumMeanDemands, maxNumMeanDemands, numMeanDemandsStep):
        stdDemands = 2/5*meanDemands/3
        lowDemands = 3/5*meanDemands
        highDemands = 7/5*meanDemands

        demands = []
        while len(demands) < numModules:
            sample = round(random.normal(meanDemands, stdDemands))
            if sample > lowDemands and sample <= highDemands:
                demands.append(sample)

        instance = {}
        instance["L"] = L
        instance["numModules"] = len(modules)
        instance["modules"] = sorted(modules)
        instance["meanDemand"] = meanDemands
        instance["demandRange"] = [lowDemands, highDemands]
        instance["demands"] = demands
        instance["isValid"] = max(modules) < L
        instances.append(instance)

    with open(outputFileName, "w") as outfile:
        json.dump(instances, outfile)


def generateInstancesWithDifferentModuleLenghtSTD(outputFileName, listStdModulesValues):
    random.seed(1)
    L = 1000
    numModules = 20

    meanModules = 100   #mean module lenght
    #stdModules = 100 / 3
    lowModules = 0      #lower bound module lenght
    highModules = 200   #upper bound module lenght


    meanDemands = 500
    stdDemands = 200 / 3
    lowDemands = 300
    highDemands = 700

    demands = []
    while len(demands) < numModules:
        sample = round(random.normal(meanDemands, stdDemands))
        if sample > lowDemands and sample <= highDemands:
            demands.append(sample)

    instances = []
    for stdModules in listStdModulesValues:

        modules = []
        while len(modules) < numModules:
            sample = round(random.normal(meanModules, stdModules))
            if sample > lowModules and sample <= highModules:
                modules.append(sample)


        instance = {}
        instance["L"] = L
        instance["stdModules"] = stdModules
        instance["modules"] = sorted(modules)
        instance["demands"] = demands
        instance["isValid"] = max(modules) < L
        instances.append(instance)

    with open(outputFileName, "w") as outfile:
        json.dump(instances, outfile)


def generateInstancesWithDifferentModuleLenghtMean(outputFileName, minModuleLenghtMean, maxModuleLenghtMean, moduleLenghtMeanStep):
    random.seed(1)
    L = 1000
    numModules = 20

  #  meanModules = 100   #mean module lenght
    stdModules = 100 / 3
    lowModules = 0      #lower bound module lenght
    highModules = 200   #upper bound module lenght


    meanDemands = 500
    stdDemands = 200 / 3
    lowDemands = 300
    highDemands = 700

    demands = []
    while len(demands) < numModules:
        sample = round(random.normal(meanDemands, stdDemands))
        if sample > lowDemands and sample <= highDemands:
            demands.append(sample)

    instances = []
    for meanModules in range(minModuleLenghtMean, maxModuleLenghtMean, moduleLenghtMeanStep):

        modules = []
        while len(modules) < numModules:
            sample = round(random.normal(meanModules, stdModules))
            if sample > max(lowModules, lowModules+(meanModules-100)) and sample <= (highModules+(meanModules-100)):
                modules.append(sample)


        instance = {}
        instance["L"] = L
        instance["meanModules"] = meanModules
        instance["modules"] = sorted(modules)
        instance["demands"] = demands
        instance["isValid"] = max(modules) < L
        instances.append(instance)

    with open(outputFileName, "w") as outfile:
        json.dump(instances, outfile)


def createJsonFiles():
    #set standard instance parameters
    #L = 1000
    #numModules = 20
    #meanModules = 100
    #stdModules = 100/3
    #lowModules = 0
    #highModules = 200
    #meanDemands = 500
    #stdDemands = 200/3
    #lowDemands = 300
    #highDemands = 700


    #generateInstancesWithDifferentPaperRollLenght(outputFileName="paperRollLenght.json", minPaperRollLenght = 100,
     #                                             maxPaperRollLenght = 10100, paperRollLenghtStep = 100)

    generateInstancesWithDifferentNumberOfModules(outputFileName="numberOfModules.json", minNumModules = 5,
                                                  maxNumModules = 205, numModulesStep = 5)

    generateInstancesWithDifferentNumberOfMeanDemands(outputFileName="meanDemands.json", minNumMeanDemands = 50,
                                                      maxNumMeanDemands = 2000, numMeanDemandsStep = 50)

    #listStdModulesValues = list(linspace(10/3, 210/3, 20, endpoint = False))
    #listStdModulesValues.extend(list(linspace(250/3, 2550/3, 46, endpoint = False)))

   # generateInstancesWithDifferentModuleLenghtSTD(outputFileName = "stdModulesLenght.json", listStdModulesValues = listStdModulesValues)

   # generateInstancesWithDifferentModuleLenghtMean(outputFileName= "meanModuleLenght.json", minModuleLenghtMean = 20,
   #                                                maxModuleLenghtMean = 400, moduleLenghtMeanStep = 20)


createJsonFiles()