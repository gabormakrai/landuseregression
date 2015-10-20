"""
File contains the code for splitting the data for Cross-Validation
"""
import random

def crossValidation(k, data, columns, targetColumn, trainFunction, applyFunction, evalFunction):
    # create group class data
    group = []
    dataCounter = {}
    for i in range(0, k):
        dataCounter[i] = 0
    for i in range(0, len(data[targetColumn])):
        g = random.randint(0, k - 1)
        group.append(g)
        dataCounter[g] = dataCounter[g] + 1
        
    print(dataCounter)
    print(columns)
        
    for iteration in range(0, k):        
        trainData = {}
        testData = {}
        # add columns for trainData and testData
        for column in columns:
            trainData[column] = []
            testData[column] = []
            
        for i in range(0, len(group)):
            if iteration == group[i]:
                targetData = testData
            else:
                targetData = trainData
    
            for column in columns:
                targetData[column].append(data[column][i])
                
        model = trainFunction(trainData, columns, targetColumn)
        
        predictionData = applyFunction(testData, model)
        
        m = evalFunction(testData[targetColumn], predictionData)
        
        print(str(m))
        
            