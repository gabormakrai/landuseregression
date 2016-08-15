"""
File contains the code for splitting the data for Cross-Validation
"""
import random
import math

def crossValidation(k, data, columns, targetColumn, normalization, trainFunction, applyFunction, evalFunctions, parameters):
    # create group class data
    group = []
    dataCounter = {}
    for i in range(0, k):
        dataCounter[i] = 0
    for i in range(0, len(data[targetColumn])):
        g = random.randint(0, k - 1)
        group.append(g)
        dataCounter[g] = dataCounter[g] + 1
        
#     print("Columns: " + str(columns))
#     print("\tGroups: " + str(dataCounter))
    
    iterationResults = []
    scatterResult = {}
    scatterResult["prediction"] = []
    scatterResult["test"] = []
        
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
                
        normalization.stat(trainData)
        
        normalization.normalize(trainData)
        
        normalization.normalize(testData)
                
        model = trainFunction(trainData, columns, targetColumn, parameters)
        
        predictionData = applyFunction(testData, model, parameters)
        
        normalization.denormalize(predictionData, targetColumn)
        len(targetData)
        normalization.denormalize(testData[targetColumn], targetColumn)
        
        for d in testData[targetColumn]:
            scatterResult["test"].append(d)
        for d in predictionData:
            scatterResult["prediction"].append(d)
        
        resultArray = []
        
        for evalFunction in evalFunctions:
            result = evalFunction(testData[targetColumn], predictionData)
            resultArray.append(result)
            
        # print("\t" + str(resultArray))
        
        iterationResults.append(resultArray)
    
    averages = {}
    
    for result in iterationResults:
        for keyvalue in result:
            key = keyvalue[0]
            value = keyvalue[1]
            if key not in averages:
                averages[key] = 0.0
            
            current = averages[key]
            current = current + value
            averages[key] = current
    
    for key in averages:
        value = averages[key]
        value = value / len(iterationResults)
        averages[key] = value
        
    dev = {}
    
    for result in iterationResults:
        for keyvalue in result:
            key = keyvalue[0]
            value = keyvalue[1]
            if key not in dev:
                dev[key] = 0.0
            
            current = dev[key]
            current = current + math.pow(value - averages[key], 2.0)
            dev[key] = current
    
    for key in averages:
        value = dev[key]
        value = value / len(iterationResults)
        value = math.sqrt(value)
        dev[key] = value
    
    return {"avg": averages, "std": dev, "scatter": scatterResult }
