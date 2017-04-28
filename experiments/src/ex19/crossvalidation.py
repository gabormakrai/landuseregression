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

def splitDataForXValidation(value, validationColumn, data, columns, allColumns, targetColumn):
    
    dataY = {}
    for c in allColumns:
        dataY[c] = []
    
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
        if data[validationColumn][i] == value:
            targetX = testX
            targetY = testY
            for c in allColumns:
                dataY[c].append(data[c][i])
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return trainX, testX, trainY, testY, dataY    
    
def generateTrainingData(data, columns):
    
    X = []
    
    for i in range(0, len(data[columns[0]])):
        x = []
        for c in columns:
            x.append(data[c][i])
        X.append(x)
    
    return X

def sample(trainRate, X, Y):
    trainX = []
    testX = []
    trainY = []
    testY = []
    
    for i in range(0, len(Y)):
        x = []
        for v in X[i]:
            x.append(v)
        if i / len(Y) < trainRate:
            trainX.append(x)
            trainY.append(Y[i])
        else:
            testX.append(x)
            testY.append(Y[i])
    
    return trainX, trainY, testX, testY
