import numpy as np
from error import raeEval, rmseEval

def hourCategory(testData, i):
    return str(testData["hour"][i])

def raeEvaluation(testData, predictionData):
    rae = raeEval(testData, predictionData)[1]
    raeMedian = np.percentile(np.array(rae), 50) 
    return raeMedian

def rmseEvaluation(testData, predictionData):
    rmse = rmseEval(testData, predictionData)[1]
    return rmse

def hourCategoryOrder(categories):
    toPrintCategories = []
    categoriesInOrder = []
    for category in categories:
        categoriesInOrder.append(float(category))
    categoriesInOrder.sort()
    for c in categoriesInOrder:
        category = str(c)
        toPrintCategories.append(category)
    return toPrintCategories

def hourPostProcessResult(modelResult):
    medianModelRes = {}
    for category in modelResult:
        median = np.percentile(np.array(modelResult[category]), 50)
        medianModelRes[category] = median 

    return medianModelRes

def windspeedCategory(testData, i):
    category = 0
    if testData["windspeed"][i] >= 3.0 and testData["windspeed"][i] < 6.0:
        category = 1
    elif testData["windspeed"][i] >= 6.0 and testData["windspeed"][i] < 9.0:
        category = 2
    elif testData["windspeed"][i] >= 9.0 and testData["windspeed"][i] < 12.0:
        category = 3
    elif testData["windspeed"][i] >= 12.0 and testData["windspeed"][i] < 15.0:
        category = 4
    elif testData["windspeed"][i] >= 15.0 and testData["windspeed"][i] < 18.0:
        category = 5
    else:
        category = 6
    
    return str(category)

def windspeedCategoryOrder(categories):
    toPrintCategories = []
    categoriesInOrder = []
    for category in categories:
        categoriesInOrder.append(int(category))
    categoriesInOrder.sort()
    for c in categoriesInOrder:
        category = str(c)
        toPrintCategories.append(category)
    return toPrintCategories
    
def windspeedPostProcessResult(modelResult):
    medianModelRes = {}
    for category in modelResult:
        median = np.percentile(np.array(modelResult[category]), 50)
        medianModelRes[category] = median 

    return medianModelRes
