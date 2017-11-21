from ex25.ex25_lib import loadEx25Data
from data.data import loadData
from ex25.crossvalidation import splitDataForXValidation
from eval.rmse import rmseEval
from _collections import defaultdict

DATA_FILE = "/data/york3_hour_2013.csv"
INPUT_FILE = "/experiments/ex25/file.csv"

predData = loadEx25Data(INPUT_FILE)
tags = set(tag for tag in predData)

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))
stationsNames = {2.0: "Fulford", 3.0: "Gillygate", 4.0: "Heworth", 6.0: "Lawrence", 8.0: "Fishergate"}
locations = [2.0, 3.0, 4.0, 6.0, 8.0]

bestCounter = defaultdict(lambda: 0)

for location in locations:
    print("location: " + stationsNames[location])
    trainX, testX, trainY, testY, _, testTimestamp = splitDataForXValidation(location, "location", data, [], "target", timestampData)    
    
    locationBestCounter = defaultdict(lambda: 0)
    
    twPredictions = []
    bestPredictions = []
    avgPredictions = []
    
    for i in range(0, len(testY)):
        bestAbs = abs(testY[i] - predData["TW"][str(location)][str(int(testTimestamp[i]))])
        bestModel = "TW"
        for tag in tags:
            tagAbs = abs(testY[i] - predData[tag][str(location)][str(int(testTimestamp[i]))])
            if tagAbs < bestAbs:
                bestModel = tag 
                bestAbs = tagAbs
        
        locationBestCounter[bestModel] = locationBestCounter[bestModel] + 1
        
        twPred = predData["TW"][str(location)][str(int(testTimestamp[i]))]
        twPredictions.append(twPred)
        
        bestPred = predData[bestModel][str(location)][str(int(testTimestamp[i]))]
        bestPredictions.append(bestPred)
                
    # print(str(locationBestCounter))
    rmse = rmseEval(testY, twPredictions)[1]
    print("\tTW rmse: " + str(rmse))
    rmse = rmseEval(testY, bestPredictions)[1]
    print("\tBest rmse: " + str(rmse))    
    for tag in tags:
        bestCounter[tag] = bestCounter[tag] + locationBestCounter[tag]

print("BestCounter:")
orderedBestCounter = []
for tag in tags:
    orderedBestCounter.append((bestCounter[tag], tag))
orderedBestCounter.sort(reverse=True)
for t in orderedBestCounter:
    print("\t" + t[1] + ": " + str(t[0]))
    