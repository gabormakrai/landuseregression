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

def splitDataForXValidation(value, validationColumn, data, columns, targetColumn, dayNight):
    
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
            # validation/test case
            targetX = testX
            targetY = testY
        if dayNight == True:
            if data[validationColumn][i] == value and data["hour"][i] > 6 and data["hour"][i] < 20:
                continue
            if data[validationColumn][i] != value and (data["hour"][i] <= 6 or data["hour"][i] >= 20):
                continue
        if dayNight == False:
            if data[validationColumn][i] != value and data["hour"][i] > 6 and data["hour"][i] < 20:
                continue
            if data[validationColumn][i] == value and (data["hour"][i] <= 6 or data["hour"][i] >= 20):
                continue
            
        X = []
        for c in columnsWithoutValidationAndTarget:
            X.append(data[c][i])
            
        Y = data[targetColumn][i]
        
        targetY.append(Y)
        targetX.append(X)
            
    return trainX, testX, trainY, testY    
    
