from copy import deepcopy

def splitDataForXValidation(trainSet, testSet, validationColumn, data, columns, targetColumn):
    
    columnsWithoutValidationAndTarget = deepcopy(columns)
    if validationColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(validationColumn)
    if targetColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(targetColumn)
    
    trainX = []
    testX = []
    trainY = []
    testY = []
    
    for i in range(0, len(data[validationColumn])):
        targetX = trainX
        targetY = trainY
        if data[validationColumn][i] in testSet:
            targetX = testX
            targetY = testY
        elif data[validationColumn][i] not in trainSet:
            continue
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return trainX, testX, trainY, testY

def splitDataForXValidationWithLocation(trainSet, testSet, validationColumn, data, columns, targetColumn):
    
    columnsWithoutValidationAndTarget = deepcopy(columns)
    if validationColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(validationColumn)
    if targetColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(targetColumn)
    
    trainX = []
    testX = []
    trainY = []
    testY = []
    trainLocation = []
    testLocation = []
    
    for i in range(0, len(data[validationColumn])):
        targetX = trainX
        targetY = trainY
        targetLocation = trainLocation
        if data[validationColumn][i] in testSet:
            targetX = testX
            targetY = testY
            targetLocation = testLocation
        elif data[validationColumn][i] not in trainSet:
            continue
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        l = data["location"][i]
        
        targetY.append(Y)
        targetX.append(X)
        targetLocation.append(l)
            
    return trainX, testX, trainY, testY, trainLocation, testLocation
