from ex27.ex27_lib import generateAllDataGroups,getTagAndFeatures
from eval.rmse import rmseEval
from sklearn.ensemble.forest import RandomForestClassifier,\
    RandomForestRegressor
from copy import deepcopy
from data.data import loadData
from ex27.crossvalidation import splitDataForXValidationSampled2
from collections import defaultdict

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_FILE = "/experiments/ex27/ex27_b.txt"

data = {}
columns = []
loadData(DATA_FILE, ['timestamp'], data, columns)

output = open(OUTPUT_FILE, 'w')

def log(message):
    print(message)
    output.write(message)
    output.write("\n")
    output.flush()

all_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc', 'lane_length', 'length', 'landuse_area', 'leisure_area', 'buildings_area', 'buildings_number']

topTags = ['TW','TWA', 'WA']
topPreds = ["pred_" + tag for tag in topTags]

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

all_columns = all_features + topPreds

topDatagroups = []
data_groups = generateAllDataGroups()

for tag in topTags:
    for datagroup in data_groups:
        dgtag, _ = getTagAndFeatures(datagroup)
        if dgtag == tag:
            topDatagroups.append(datagroup)
            break

def evalColumns(columns):

    overallY = []
    overallPred = []

    for location in locations:
        location2s = [l for l in locations if l != location]
        
        print("Location: " + str(location) + ", location2: " + str(location2s))
          
        trainPreds = defaultdict(list)
        testPreds = defaultdict(list)
          
        for datagroup in topDatagroups:
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
            bestAbs = abs(t2Y[i] - trainPreds[topTags[0]][i])
            for j in range(0, len(topTags)):
                tag = topTags[j]
                modelAbs = abs(t2Y[i] - trainPreds[tag][i])
                if modelAbs < bestAbs:
                    bestAbs = modelAbs
                    bestModel = j
            labelt2Y.append(bestModel)
             
        print("#labelt2Y:" + str(len(labelt2Y)))
        tX2 = []
        testX = []
        for location2 in location2s:
            trainX1, trainX2, trainY1, trainY2, tX, testY = splitDataForXValidationSampled2(location, location2, "location", data, all_features, "target")
            for row in trainX2:
                tX2.append(row)
            for row in tX:
                testX.append(row)
        
        for pred in topTags:
            for i in range(0, len(trainPreds[tag])):
                tX2[i].append(trainPreds[tag][i]) 
        
        reducedTrainX2 = []
        for d in tX2:
            reducedD = []
            for i in range(0, len(all_columns)):
                if columns[i]:
                    reducedD.append(d[i])
            reducedTrainX2.append(reducedD)
              
        model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=15)
        model.fit(reducedTrainX2, labelt2Y)
        
        for pred in topTags:
            for i in range(0, len(testPreds[tag])):
                testX[i].append(testPreds[tag][i]) 
        
        reducedTestX = []
        for d in testX:
            reducedD = []
            for i in range(0, len(all_columns)):
                if columns[i]:
                    reducedD.append(d[i])
            reducedTestX.append(reducedD)
         
        pred = model.predict(reducedTestX)
         
        finalPrediction = []
        for i in range(0, len(testY)):
            p = testPreds[topTags[pred[i]]][i]
            finalPrediction.append(p)      
        rmse = str(rmseEval(testY, finalPrediction)[1])
        print("\tRMSE: " + str(rmse))
        
        for x in testY:
            overallY.append(x)
        for x in finalPrediction:
            overallPred.append(x)
    
    rmse = rmseEval(overallPred, overallY)[1]
    return rmse

def generatePossibleSteps(currentColumns):
    nextSteps = []
    
    l = len(currentColumns)
    enabled = len([1 for c in currentColumns if c])
    if (l != enabled):
        for i in range(0, len(currentColumns)):
            if currentColumns[i]:
                continue
            step = deepcopy(currentColumns)
            step[i] = True
            nextSteps.append(step)
        
    for i in range(0, len(currentColumns)):
        if not currentColumns[i]:
            continue
        step = deepcopy(currentColumns)
        step[i] = False
        nextSteps.append(step)
    
    return nextSteps

currentColumns = [True for c in all_columns]
bestSoFarColumns = deepcopy(currentColumns)
bestSoFarRmse = 1000.0

for iteration in range(0, 1000000):
    log("BestSoFar: " + str(bestSoFarRmse) + " <- " + str(bestSoFarColumns))
    
    steps = generatePossibleSteps(currentColumns)
        
    rmses = []
    for step in steps:
        rmse = evalColumns(step)
        log("\t" + str(rmse) + " <- " + str(step))
        rmses.append(rmse)
    iterationBest = None
    iterationBestRmse = 1000.0
    for i in range(0, len(rmses)):
        if rmses[i] < iterationBestRmse:
            iterationBestRmse = rmses[i]
            iterationBest = steps[i]
    log("iterationBest: " + str(iterationBestRmse) + " <- " + str(iterationBest))
    if iterationBestRmse < bestSoFarRmse:
        bestSoFarRmse = iterationBestRmse
        bestSoFarColumns = iterationBest
        
    previousBestRmse = iterationBestRmse
    currentColumns = iterationBest
        
output.close()
