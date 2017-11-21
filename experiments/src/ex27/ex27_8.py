from data.data import loadData
from ex27.crossvalidation import splitDataForXValidationSampled2
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
from ex27.ex27_lib import generateAllDataGroups, getTagAndFeatures
from collections import defaultdict

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_DIRECTORY = "/experiments/ex27/"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, ['timestamp'], data, columns)

sampleRate = 0.75

all_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc', 'lane_length', 'length', 'landuse_area', 'leisure_area', 'buildings_area', 'buildings_number']

top10tags = ['TW','TWA','W','TWL','TWB','T','WA','WB','TA','A']
top10tags = ['TW','TWA','TWL']
top10tags = ['TW','TWA', 'WA']

top10datagroups = []
data_groups = generateAllDataGroups()

for tag in top10tags:
    for datagroup in data_groups:
        dgtag, _ = getTagAndFeatures(datagroup)
        if dgtag == tag:
            top10datagroups.append(datagroup)
            break

allPrediction = []
allObs = []
 
for location in locations:
    location2s = [l for l in locations if l != location]
    
    print("Location: " + str(location) + ", location2: " + str(location2s))
      
    trainPreds = defaultdict(list)
    testPreds = defaultdict(list)
      
    for datagroup in top10datagroups:
        tag, features = getTagAndFeatures(datagroup)
        print("\ttag: " + str(tag) + ", features: " + str(features))
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
            print("\t\ttrain1 rmse: " + train1Rmse)
            print("\t\ttrain2 rmse: " + train2Rmse)
            print("\t\ttest rmse: " + testRmse)
            for x in train2Prediction:
                trainPreds[tag].append(x)
            for x in testPrediction:
                testPreds[tag].append(x)
            
    t2Y = []        
    for location2 in location2s:
        trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled2(location, location2, "location", data, all_features, "target")
        t2Y = t2Y + trainY2
      
    labelt2Y = []
      
    for i in range(0, len(t2Y)):
        bestModel = 0
        bestAbs = abs(t2Y[i] - trainPreds[top10tags[0]][i])
        for j in range(0, len(top10tags)):
            tag = top10tags[j]
            modelAbs = abs(t2Y[i] - trainPreds[tag][i])
            if modelAbs < bestAbs:
                bestAbs = modelAbs
                bestModel = j
        labelt2Y.append(bestModel)
         
    print("#labelt2Y:" + str(len(labelt2Y)))
    tX2 = []
    for location2 in location2s:
        trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled2(location, location2, "location", data, all_features, "target")
        for row in trainX2:
            tX2.append(row)
          
    model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=15)
    model.fit(tX2, labelt2Y)
     
    pred = model.predict(testX)
     
    finalPrediction = []
    for i in range(0, len(testY)):
        p = testPreds[top10tags[pred[i]]][i]
        finalPrediction.append(p)      
    rmse = str(rmseEval(testY, finalPrediction)[1])
    print("\tRMSE: " + str(rmse))
    
    for x in testY:
        allObs.append(x)
    for x in finalPrediction:
        allPrediction.append(x)
    
print("Overall")    
rmse = str(rmseEval(allObs, allPrediction)[1])
print("\tRMSE: " + str(rmse))
