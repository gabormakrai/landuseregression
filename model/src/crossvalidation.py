"""
File contains the code for splitting the data for Cross-Validation
"""
import random
import math
from copy import deepcopy

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

def crossValidationHour(k, data, columns, targetColumn, normalization, trainFunction, applyFunction, evalFunctions, parameters):
    # create group class data
    group = []
    dataCounter = {}
    for i in range(0, k):
        dataCounter[i] = 0
    for i in range(0, len(data[targetColumn])):
        g = random.randint(0, k - 1)
        group.append(g)
        dataCounter[g] = dataCounter[g] + 1
            
    iterationResults = []
        
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
        
        normalization.denormalize(testData[targetColumn], targetColumn)
        
#         for d in testData[targetColumn]:
#             scatterResult["test"].append(d)
#         for d in predictionData:
#             scatterResult["prediction"].append(d)
        
        testHour = {}
        predictionHour = {}
        
        for i in range(0,24):
            testHour[i] = []
            predictionHour[i] = []
            
        for i in range(0,len(testData[targetColumn])):
            if "hour" in testData:
                hour = testData["hour"][i]
            else:
                for j in range(0,24):
                    if testData["hour" + str(j)][i] > 0.5:
                        hour = j
                        break
            testHour[hour].append(testData[targetColumn][i])
            predictionHour[hour].append(predictionData[i])
        
        result = {}
        
        for evalFunction in evalFunctions:
            for hour in range(0,24):
                r = evalFunction(testHour[hour], predictionHour[hour]) 
                # r[0]: name
                # r[1]: value
                if r[0] not in result:
                    result[r[0]] = {}
                result[r[0]][hour] = r[1]
        
        iterationResults.append(result)
    
    averages = {}
    
    for result in iterationResults:
        for evalName in result:
            if evalName not in averages:
                averages[evalName] = {}
            for hour in result[evalName]:
#                print("evalName:" + str(evalName) + ",h:" + str(hour))
                if hour not in averages[evalName]:
                    averages[evalName][hour] = []
                value = result[evalName][hour]
                averages[evalName][hour].append(value)

    returnValue = {}
    
    for evalName in averages:
        if evalName not in returnValue:
            returnValue[evalName] = {}
        for hour in averages[evalName]:
            values = averages[evalName][hour]
            avg = 0.0
            for v in values:
                avg = avg + v
            avg = avg / float(len(values))
            returnValue[evalName][hour] = avg
    
    return returnValue

def crossValidationLocation(data, columns, targetColumn, normalization, trainFunction, applyFunction, evalFunctions, parameters):
    
    # find out k
    locationSet = set()
    
    for loc in data["location"]:
        locationSet.add(loc)

    # assign id for each location
    locationId = {}
    for loc in locationSet:
        ID = len(locationId)
        locationId[str(loc)] = ID
        
    k = len(locationId)
         
    # create group class data
    group = []
    dataCounter = {}
    for i in range(0, k):
        dataCounter[i] = 0
                
    for i in range(0, len(data[targetColumn])):
        loc = str(data["location"][i])
        g = locationId[loc]
        group.append(g)
        dataCounter[g] = dataCounter[g] + 1
         
    print("Columns: " + str(columns))
    print("\tGroups: " + str(dataCounter))
    
    #delete location data
    del data["location"]
    #delete location column
    columns.remove("location")
    
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
        
        normalization.denormalize(testData[targetColumn], targetColumn)

        if iteration == 0:
            for d in testData[targetColumn]:
                scatterResult["test"].append(d)
            for d in predictionData:
                scatterResult["prediction"].append(d)
         
        resultArray = []
         
        for evalFunction in evalFunctions:
            result = evalFunction(testData[targetColumn], predictionData)
            resultArray.append(result)
             
        #print("\t" + str(resultArray))
        
#         for j in range(0, len(testData[targetColumn])):
#             print("asd " + str(testData[targetColumn][j]) + " <-> " + str(predictionData[j]))
         
        iterationResults.append(resultArray)
     
    averages = {}
    
    evalResult = {}
     
    for result in iterationResults:
        for keyvalue in result:
            key = keyvalue[0]
            value = keyvalue[1]
            if key not in evalResult:
                evalResult[key] = []
            evalResult[key].append(value)
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
     
    return {"avg": averages, "std": dev, "scatter": scatterResult, "eval": evalResult }

def crossValidationLocationHour(data, columns, targetColumn, normalization, trainFunction, applyFunction, evalFunctions, parameters):
    
    # find out k
    locationSet = set()
    
    for loc in data["location"]:
        locationSet.add(loc)

    # assign id for each location
    locationId = {}
    for loc in locationSet:
        ID = len(locationId)
        locationId[str(loc)] = ID
        
    k = len(locationId)
         
    # create group class data
    group = []
    dataCounter = {}
    for i in range(0, k):
        dataCounter[i] = 0
                
    for i in range(0, len(data[targetColumn])):
        loc = str(data["location"][i])
        g = locationId[loc]
        group.append(g)
        dataCounter[g] = dataCounter[g] + 1
         
    print("Columns: " + str(columns))
    print("\tGroups: " + str(dataCounter))
    
    #delete location data
    del data["location"]
    #delete location column
    columns.remove("location")
            
    iterationResults = []
        
    for iteration in range(0, k): 
        
        trainData = {}
        testData = {}
        # add columns for trainData and testData
        for column in columns:
            trainData[column] = []
            testData[column] = []
             
        testData["hour"] = []
        
        for i in range(0, len(group)):
            if iteration == group[i]:
                if "hour" not in columns:
                    testData["hour"].append(data["hour"][i])
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
        
        normalization.denormalize(testData[targetColumn], targetColumn)
        
#         for d in testData[targetColumn]:
#             scatterResult["test"].append(d)
#         for d in predictionData:
#             scatterResult["prediction"].append(d)
        
        testHour = {}
        predictionHour = {}
        
        for i in range(0,24):
            testHour[i] = []
            predictionHour[i] = []
            
        for i in range(0,len(testData[targetColumn])):
            if "hour" in testData:
                hour = testData["hour"][i]
            else:
                for j in range(0,24):
                    if testData["hour" + str(j)][i] > 0.5:
                        hour = j
                        break
#             print(str(hour))
            testHour[hour].append(testData[targetColumn][i])
            predictionHour[hour].append(predictionData[i])
        
        result = {}
        
        for evalFunction in evalFunctions:
            for hour in range(0,24):
                r = evalFunction(testHour[hour], predictionHour[hour]) 
                # r[0]: name
                # r[1]: value
                if r[0] not in result:
                    result[r[0]] = {}
                result[r[0]][hour] = r[1]
        
        iterationResults.append(result)
    
    averages = {}
    
    for result in iterationResults:
        for evalName in result:
            if evalName not in averages:
                averages[evalName] = {}
            for hour in result[evalName]:
#                print("evalName:" + str(evalName) + ",h:" + str(hour))
                if hour not in averages[evalName]:
                    averages[evalName][hour] = []
                value = result[evalName][hour]
                averages[evalName][hour].append(value)

    returnValue = {}
    evalResult = deepcopy(averages)
    
    for evalName in averages:
        if evalName not in returnValue:
            returnValue[evalName] = {}
        for hour in averages[evalName]:
            values = averages[evalName][hour]
            avg = 0.0
            for v in values:
                avg = avg + v
            avg = avg / float(len(values))
            returnValue[evalName][hour] = avg
    
    return {"avg": returnValue, "eval": evalResult}
