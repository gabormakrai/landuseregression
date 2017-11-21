from data.data import loadData
from ex25.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval

DATA_FILE = "/data/york3_hour_2013.csv"

tags = ['TWL', 'TW', 'TWA', 'AL', 'WA', 'A' , 'W', 'TA', 'TL', 'TWB', 'TWAL', 'WL', 'TR', 'WAR', 'WAL', 'TWR'] 
tags = ['TWL', 'TW', 'TWA', 'AL', 'WA'] # , 'A' , 'W', 'TA', 'TL', 'TWB', 'TWAL', 'WL', 'TR', 'WAR', 'WAL', 'TWR'] 

tagSet = set(tags)
tags_ids = {tags[i]: i for i in range(0, len(tags))} 

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))

columnsGrouped = {
    "T": ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day'],
    "W": ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure'],
    "A": ['atc'],
    "R": ['lane_length', 'length'],
    "L": ['landuse_area', 'leisure_area'],
    "B": ['buildings_area', 'buildings_number']
    }

def getFeatures(dataGroup):
    features = []
    for dg in dataGroup:
        for d in columnsGrouped[dg]:
            features.append(d)
    return features
        
for location in locations:
    print("\tlocation: " + str(location))
    
    trainPredictions = {}
    testPredictions = {}
        
    for tag in tags:
#         print("\t\t" + tag)
        features = getFeatures(tag)
        trainX, testX, trainY, testY, _, _ = splitDataForXValidation(location, "location", data, features, "target", timestampData)
#         print("\t\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        trainPrediction = model.predict(trainX)
        testPrediction = model.predict(testX)
#         print("\t\trmse: " + str(rmseEval(trainY, trainPrediction)[1]))
#         print("\t\trmse: " + str(rmseEval(testY, testPrediction)[1]))
        trainPredictions[tag] = trainPrediction
        testPredictions[tag] = testPrediction

    features = getFeatures("TWAB")                
    trainX, testX, trainY, testY, _, _ = splitDataForXValidation(location, "location", data, features, "target", timestampData)

    label = []
    for i in range(0, len(trainPredictions['TW'])):
        bestAbs = abs(trainPredictions['TW'][i] - trainY[i])
        bestTag = 'TW'
        for tag in tags:
            tagAbs = abs(trainPredictions[tag][i] - trainY[i])
            if tagAbs < bestAbs:
                bestAbs = tagAbs
                bestTag = tag
        label.append(tags_ids[bestTag])
    
    # model = OneVsRestClassifier(estimator=SVC(random_state=42))
    model = RandomForestClassifier(n_estimators=100, random_state=42) 
    model.fit(trainX, label)

    pred = model.predict(testX)
    finalPredictions = []
    for i in range(0, len(pred)):
        t = tags[int(round(pred[i]))]
        p = testPredictions[t][i]
        finalPredictions.append(p)
        
    rmse = rmseEval(testY, testPredictions["TW"])[1]
    print("\tTW rmse: " + str(rmse))
    
    rmse = rmseEval(testY, finalPredictions)[1]
    print("\tFinal rmse: " + str(rmse))
    