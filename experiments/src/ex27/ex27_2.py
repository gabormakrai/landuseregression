from data.data import loadData
from ex27.crossvalidation import splitDataForXValidationSampled
from sklearn.ensemble.forest import RandomForestRegressor
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

data_groups = generateAllDataGroups()
tags = [getTagAndFeatures(datagroup)[0] for datagroup in data_groups]
top10tags = ['TW','TWA','W','TWL','TWB','T','WA','WB','TA','A']

overAllFreq = defaultdict(lambda: 0)
overAllFreqT16 = defaultdict(lambda: 0)

for location in locations:
    print("Location: " + str(location))
    
    trainPreds = {}
    testPreds = {}
    t2Y = None
    tY = None
    
    for datagroup in data_groups:
        tag, features = getTagAndFeatures(datagroup)
        print("\ttag: " + str(tag) + ", features: " + str(features))
        trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled(location, "location", sampleRate, 42, data, features, "target")
        t2Y = trainY2
        tY = testY
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
        trainPreds[tag] = train2Prediction
        testPreds[tag] = testPrediction
        
    labelt2Y = []
    
    for i in range(0, len(t2Y)):
        bestModel = 0
        bestAbs = abs(t2Y[i] - trainPreds[tags[0]][i])
        for j in range(0, len(tags)):
            tag = tags[j]
            modelAbs = abs(t2Y[i] - trainPreds[tag][i])
            if modelAbs < bestAbs:
                bestAbs = modelAbs
                bestModel = j
        labelt2Y.append(bestModel)
    
    freq = defaultdict(lambda: 0)
    for l in labelt2Y:
        freq[l] = freq[l] + 1
        overAllFreq[l] = overAllFreq[l] + 1
            
    print("\tBestCounter:")
    orderedBestCounter = []
    for i in range(0, len(tags)):
        orderedBestCounter.append((freq[i], tags[i]))
    orderedBestCounter.sort(reverse=True)
    for t in orderedBestCounter:
        print("\t\t" + t[1] + ": " + str(t[0]))
    
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
    
    freq = defaultdict(lambda: 0)
    for l in labelt2Y:
        freq[l] = freq[l] + 1
        overAllFreqT16[l] = overAllFreqT16[l] + 1
            
    print("\tBestCounterT16:")
    orderedBestCounter = []
    for i in range(0, len(top10tags)):
        orderedBestCounter.append((freq[i], top10tags[i]))
    orderedBestCounter.sort(reverse=True)
    for t in orderedBestCounter:
        print("\t\t" + t[1] + ": " + str(t[0]))
    
    
print("BestCounter:")
orderedBestCounter = []
for i in range(0, len(tags)):
    orderedBestCounter.append((overAllFreq[i], tags[i]))
orderedBestCounter.sort(reverse=True)
for t in orderedBestCounter:
    print("\t" + t[1] + ": " + str(t[0]))

print("BestCounterT16:")
orderedBestCounter = []
for i in range(0, len(top10tags)):
    orderedBestCounter.append((overAllFreqT16[i], top10tags[i]))
orderedBestCounter.sort(reverse=True)
for t in orderedBestCounter:
    print("\t" + t[1] + ": " + str(t[0]))
    