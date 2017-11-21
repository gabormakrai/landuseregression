from copy import deepcopy

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

def splitDataForXValidation2(value, validationColumn, data, columns, targetColumn, timestampData):

    locationData = data["location"]
    
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
    trainLocation = []
    testLocation = []
        
    for i in range(0, len(data[validationColumn])):
        targetX = trainX
        targetY = trainY
        if data[validationColumn][i] == value:
            targetX = testX
            targetY = testY
            testTimestamp.append(timestampData[i])
            testLocation.append(locationData[i])
        else:
            trainTimestamp.append(timestampData[i])
            trainLocation.append(locationData[i])
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return trainX, testX, trainY, testY, trainTimestamp, testTimestamp, trainLocation, testLocation    

