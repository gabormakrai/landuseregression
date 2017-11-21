from data.data import loadData
from ex28.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor, RandomForestClassifier
from eval.rmse import rmseEval
from collections import defaultdict
from ex28.crossvalidation import splitDataForXValidationSampled2
from ex28.ex28_lib import log

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_FILE = "/experiments/ex28/ex28_3_data.csv"
OUTPUT_LOG_FILE = "/experiments/ex28/ex28_3.txt"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

steps = [
    [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
    [True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, False],
    [True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, True, False],
    [True, True, True, True, True, True, True, True, True, True, False, True, True, False, True, False, True, True, False],
    [True, True, True, True, True, True, True, True, True, True, False, True, True, False, True, False, False, True, False],
    [True, True, True, True, True, False, True, True, True, True, False, True, True, False, True, False, False, True, False]
]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))

all_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc', 'lane_length', 'length', 'landuse_area', 'leisure_area', 'buildings_area', 'buildings_number']
tw_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure'] 
twa_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc'] 

combinedTags = ["TW", "TWA"]

combinedFeatures = {
    "TW": ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure'],
    "TWA": ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc']
}

allObs = []

output = open(OUTPUT_FILE, 'w')
output.write("step,rmse_tw,rmse_twa,rmse_combined,accuracy\n")

output_log = open(OUTPUT_LOG_FILE, 'w')

log(output_log, "Generating Rmse RF+TW and Rmse RF+TWA")

allPredictionTW = []
allPredictionTWA = []
 
for location in locations:
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, tw_features, "target", timestampData)
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
    model.fit(trainX, trainY)
    testPredictionTW = model.predict(testX)
    rmse = str(rmseEval(testY, testPredictionTW)[1])
    log(output_log, "\tTW rmse: " + rmse)
    for x in testY:
        allObs.append(x)
    for x in testPredictionTW:
        allPredictionTW.append(x)
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, twa_features, "target", timestampData)
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
    model.fit(trainX, trainY)
    testPredictionTWA = model.predict(testX)
    rmse = str(rmseEval(testY, testPredictionTWA)[1])
    log(output_log, "\tTWA rmse: " + rmse)
    for x in testPredictionTWA:
        allPredictionTWA.append(x)
  
rmseTW = str(rmseEval(allObs, allPredictionTW)[1])
log(output_log, "TW RMSE: " + str(rmseTW))
rmseTWA = str(rmseEval(allObs, allPredictionTWA)[1])
log(output_log, "TWA RMSE: " + str(rmseTWA))

log(output_log, "Generating combined for each step")

for step in range(0, len(steps)):
    combined_enabled_features = steps[step]
    allPredictionCombined = []
    allTestLabel = []
    allPredLabel = []
    
    print(str(combined_enabled_features))
 
    for location in locations:
     
        location2s = [l for l in locations if l != location]
         
        # generating testPreds
        testPreds = {}
        for tag in combinedFeatures:
            features = combinedFeatures[tag]
            trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, features, "target", timestampData)
                 
            model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
            model.fit(trainX, trainY)
            prediction = model.predict(testX)
            testPreds[tag] = prediction
           
        trainPreds = defaultdict(list)
           
        for tag in combinedFeatures:
            features = combinedFeatures[tag]
            for location2 in location2s:
                trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled2(location, location2, "location", data, features, "target")
                model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
                model.fit(trainX1, trainY1)
                train1Prediction = model.predict(trainX1)
                train2Prediction = model.predict(trainX2)
                testPrediction = model.predict(testX)
                train1Rmse = str(rmseEval(trainY1, train1Prediction)[1])
                train2Rmse = str(rmseEval(trainY2, train2Prediction)[1])
                testRmse = str(rmseEval(testY, testPrediction)[1])
                for x in train2Prediction:
                    trainPreds[tag].append(x)
     
        # get combined train2y                
        combinedTrain2Y = []        
        for location2 in location2s:
            trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled2(location, location2, "location", data, all_features, "target")
            combinedTrain2Y = combinedTrain2Y + trainY2
           
        # calculate labels 
        labelTrain2Y = []
        for i in range(0, len(combinedTrain2Y)):
            bestModel = 0
            bestAbs = abs(combinedTrain2Y[i] - trainPreds[combinedTags[0]][i])
            for j in range(0, len(combinedTags)):
                tag = combinedTags[j]
                modelAbs = abs(combinedTrain2Y[i] - trainPreds[tag][i])
                if modelAbs < bestAbs:
                    bestAbs = modelAbs
                    bestModel = j
            labelTrain2Y.append(bestModel)
             
        # generating testX
        _, testX, _, _, _, _ = splitDataForXValidation(location, "location", data, all_features, "target", timestampData)
     
        # trainX2             
        tX2 = []
        for location2 in location2s:
            _, trainX2, _, _, _, _ = splitDataForXValidationSampled2(location, location2, "location", data, all_features, "target")
            for row in trainX2:
                tX2.append(row)
         
        for tag in combinedTags:
            for i in range(0, len(trainPreds[tag])):
                tX2[i].append(trainPreds[tag][i]) 
         
        reducedTrainX2 = []
        for d in tX2:
            reducedD = []
            for i in range(0, len(combined_enabled_features)):
                if combined_enabled_features[i]:
                    reducedD.append(d[i])
            reducedTrainX2.append(reducedD)
               
        model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=15)
        model.fit(reducedTrainX2, labelTrain2Y)
         
        for tag in combinedTags:
            for i in range(0, len(testPreds[tag])):
                testX[i].append(testPreds[tag][i]) 
         
        reducedTestX = []
        for d in testX:
            reducedD = []
            for i in range(0, len(combined_enabled_features)):
                if combined_enabled_features[i]:
                    reducedD.append(d[i])
            reducedTestX.append(reducedD)
          
        pred = model.predict(reducedTestX)
          
        finalPrediction = []
        for i in range(0, len(testY)):
            p = testPreds[combinedTags[pred[i]]][i]
            finalPrediction.append(p)      
        rmse = str(rmseEval(testY, finalPrediction)[1])             
        log(output_log, "\tCombined RMSE: " + str(rmse))
        
        testLabel = []
        for i in range(0, len(testY)):
            if abs(testPreds["TW"][i] - testY[i]) < abs(testPreds["TWA"][i] - testY[i]):
                testLabel.append(0)
            else:
                testLabel.append(1)
        accuracy = 0
        for i in range(0, len(testY)):
            if testLabel[i] == pred[i]:
                accuracy = accuracy + 1
        accuracy = float(accuracy) / float(len(testY)) 
        log(output_log, "\tCombined accuracy: " + str(accuracy))
        allTestLabel.extend(testLabel)
        allPredLabel.extend(pred)
         
        for p in finalPrediction:
            allPredictionCombined.append(p)
         
    log(output_log, "Overall")    
    rmse = str(rmseEval(allObs, allPredictionCombined)[1])
    log(output_log, "Combined RMSE: " + str(rmse))
    accuracy = 0
    for i in range(0, len(allTestLabel)):
        if allTestLabel[i] == allPredLabel[i]:
            accuracy = accuracy + 1
    accuracy = float(accuracy) / float(len(allTestLabel)) 
    log(output_log, "Combined accuracy: " + str(accuracy))
    
    output.write(str(step))
    output.write(",")
    output.write(str(rmseTW))
    output.write(",")
    output.write(str(rmseTWA))
    output.write(",")
    output.write(str(rmse))
    output.write(",")
    output.write(str(accuracy))
    output.write("\n")
    output.flush()
 
output.close()
output_log.close()
