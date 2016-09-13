import numpy as np
from copy import deepcopy

def findOutKForValidation(validationColumn, data):
    
    values = {}
    
    for i in range(0, len(data[validationColumn])):
        value = data[validationColumn][i]
        if value in values:
            counter = values[value]
            counter = counter + 1
            values[value] = counter
        else:
            values[value] = 1
    
    print(str(values))
    
    valueArray = []
    for v in values:
        valueArray.append(v)
    
    return valueArray

def splitDataForXValidation(value, validationColumn, data):
    trainData = {}
    testData = {}
    
    for c in data:
        if c != validationColumn:
            trainData[c] = []
            testData[c] = []
    
    for i in range(0, len(data[validationColumn])):
        targetData = trainData
        if data[validationColumn][i] == value:
            targetData = testData
        
        for c in targetData:
            targetData[c].append(data[c][i])
    
    return trainData, testData
    
    
    