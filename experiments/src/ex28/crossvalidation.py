from copy import deepcopy
import random

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

def splitDataForXValidationSampled(value, validationColumn, sampleRate, seed, data, columns, targetColumn):
    
    random.seed(seed)
    
    columnsWithoutValidationAndTarget = deepcopy(columns)
    if validationColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(validationColumn)
    if targetColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(targetColumn)
    
    trainX1 = []
    trainX2 = []
    testX = []
    trainY1 = []
    trainY2 = []
    testY = []
        
    for i in range(0, len(data[validationColumn])):
        targetX = None
        targetY = None
        if data[validationColumn][i] == value:
            targetX = testX
            targetY = testY
        elif random.random() < sampleRate:
            targetX = trainX1
            targetY = trainY1
        else:
            targetX = trainX2
            targetY = trainY2
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return trainX1, trainX2, trainY1, trainY2, testX, testY     

def splitDataForXValidationSampled2(value1, value2, validationColumn, data, columns, targetColumn):
        
    columnsWithoutValidationAndTarget = deepcopy(columns)
    if validationColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(validationColumn)
    if targetColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(targetColumn)
    
    trainX1 = []
    trainX2 = []
    testX = []
    trainY1 = []
    trainY2 = []
    testY = []
        
    for i in range(0, len(data[validationColumn])):
        targetX = None
        targetY = None
        if data[validationColumn][i] == value1:
            targetX = testX
            targetY = testY
        elif data[validationColumn][i] == value2:
            targetX = trainX2
            targetY = trainY2
        else:
            targetX = trainX1
            targetY = trainY1
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return trainX1, trainX2, trainY1, trainY2, testX, testY     

