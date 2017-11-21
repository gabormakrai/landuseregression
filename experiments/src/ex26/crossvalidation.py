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

def splitDataForXValidation2(trainSet, trainSet2, testSet, validationColumn, data, columns, targetColumn):
    
    columnsWithoutValidationAndTarget = deepcopy(columns)
    if validationColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(validationColumn)
    if targetColumn in columnsWithoutValidationAndTarget:
        columnsWithoutValidationAndTarget.remove(targetColumn)
    
    train1X = []
    train1Y = []
    train2X = []
    train2Y = []
    testX = []
    testY = []
    
    for i in range(0, len(data[validationColumn])):
        targetX = train1X
        targetY = train1Y
        if data[validationColumn][i] in testSet:
            targetX = testX
            targetY = testY
        elif data[validationColumn][i] in trainSet2:
            targetX = train2X
            targetY = train2Y
        elif data[validationColumn][i] not in trainSet:
            continue
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return train1X, train2X, testX, train1Y, train2Y, testY

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
