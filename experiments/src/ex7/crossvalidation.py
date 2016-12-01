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

def splitDataForXValidation(value, validationColumn, data, columns, targetColumn, timestampData):
    
    columnsWithoutValidationAndTarget = deepcopy(columns)
    if validationColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(validationColumn)
    if targetColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(targetColumn)
    
    trainX = []
    testX = []
    trainY = []
    testY = []
    trainTimestamp = []
    testTimestamp = []
        
    for i in range(0, len(data[validationColumn])):
        targetX = trainX
        targetY = trainY
        if data[validationColumn][i] == value:
            targetX = testX
            targetY = testY
            testTimestamp.append(timestampData[i])
        else:
            trainTimestamp.append(timestampData[i])
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return trainX, testX, trainY, testY, trainTimestamp, testTimestamp    
    
def splitDataForXValidation2(value, validationColumn, data, columns, targetColumn):
    
    columnsWithoutValidationAndTarget = deepcopy(columns)
    if validationColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(validationColumn)
    if targetColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(targetColumn)
    
    # find out array sizes
    
    trainSize = 0
    testSize = 0
    
    for i in range(0, len(data[validationColumn])):
        if data[validationColumn][i] == value:
            testSize = testSize + 1
        else:
            trainSize = trainSize + 1
            
    trainX = np.zeros((trainSize, len(columnsWithoutValidationAndTarget)))
    testX = np.zeros((testSize, len(columnsWithoutValidationAndTarget)))
    trainY = np.zeros(trainSize)
    testY = np.zeros(testSize)
    
    trainIndex = 0
    testIndex = 0
    
    for i in range(0, len(data[validationColumn])):
        targetX = trainX
        targetY = trainY
        index = trainIndex
        trainIndex = trainIndex + 1
        if data[validationColumn][i] == value:
            targetX = testX
            targetY = testY
            index = testIndex
            trainIndex = trainIndex - 1
            testIndex = testIndex + 1
        
        for j in range(0, len(columnsWithoutValidationAndTarget)):
            targetX[index][j] = data[columnsWithoutValidationAndTarget[j]][i] 
        
        targetY[index] = data[targetColumn][i]
            
    return trainX, testX, trainY, testY    
    