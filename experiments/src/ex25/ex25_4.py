from ex25.ex25_lib import loadEx25Data
from data.data import loadData
from ex25.crossvalidation import splitDataForXValidation
from eval.rmse import rmseEval
from sklearn.svm.classes import SVC
from sklearn.multiclass import OneVsRestClassifier

DATA_FILE = "/data/york3_hour_2013.csv"
INPUT_FILE = "/experiments/ex25/file.csv"

features_ALL = ['leisure_area', 'rain', 'temperature', 'atc', 'windspeed', 'lane_length', 'buildings_area', 'winddirection', 'landuse_area', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'buildings_number', 'length']

predData = loadEx25Data(INPUT_FILE)
tags = ['TWL', 'TW', 'TWA', 'AL', 'WA', 'A' , 'W', 'TA', 'TL', 'TWB', 'TWAL', 'WL', 'TR', 'WAR', 'WAL', 'TWR'] 
tagSet = set(tags)
tags_ids = {tags[i]: i for i in range(0, len(tags))} 

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))
stationsNames = {2.0: "Fulford", 3.0: "Gillygate", 4.0: "Heworth", 6.0: "Lawrence", 8.0: "Fishergate"}
locations = [2.0, 3.0, 4.0, 6.0, 8.0]

for location in locations:
    print("location: " + stationsNames[location])
    trainX, testX, trainY, testY, _, testTimestamp = splitDataForXValidation(location, "location", data, features_ALL, "target", timestampData)    

    label = []
    twPredictions = []
    bestPredictions = []
    
    for i in range(0, len(testY)):
        bestAbs = abs(testY[i] - predData["TW"][str(location)][str(int(testTimestamp[i]))])
        bestModel = "TW"
        for tag in tags:
            tagAbs = abs(testY[i] - predData[tag][str(location)][str(int(testTimestamp[i]))])
            if tagAbs < bestAbs:
                bestModel = tag 
                bestAbs = tagAbs
                
        twPred = predData["TW"][str(location)][str(int(testTimestamp[i]))]
        twPredictions.append(twPred)
        bestPred = predData[bestModel][str(location)][str(int(testTimestamp[i]))]
        bestPredictions.append(bestPred)
        label.append(tags_ids[bestModel])
                
#     model = RandomForestRegressor(min_samples_leaf = 50, n_estimators = 100, n_jobs = -1, random_state=42)
    model = OneVsRestClassifier(estimator=SVC(random_state=42))
    model.fit(testX, label)

    pred = model.predict(testX)
    print(str(pred))
    mixPreds = []
    for i in range(0, len(pred)):
        m = tags[int(round(pred[i]))]
        mixPred = predData[m][str(location)][str(int(testTimestamp[i]))]
        mixPreds.append(mixPred)
    
    rmse = rmseEval(testY, twPredictions)[1]
    print("\tTW rmse: " + str(rmse))
    rmse = rmseEval(testY, bestPredictions)[1]
    print("\tBest rmse: " + str(rmse))
    rmse = rmseEval(testY, mixPreds)[1]
    print("\tMix rmse: " + str(rmse))
    