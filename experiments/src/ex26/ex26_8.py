from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from ex26.crossvalidation import splitDataForXValidation, splitDataForXValidationWithLocation
from eval.rmse import rmseEval

all_stations = ['71.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0']

groups = [['71.0', '70.0', '38.0', '55.0', '73.0', '89.0'],
['29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0']]

DATA_FILE = "/data/london3_hour_2016.csv"

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

features_TW = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week']
features_TWA = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'atc']
features_ALL = ['leisure_area', 'rain', 'temperature', 'atc', 'windspeed', 'lane_length', 'building_area', 'winddirection', 'landuse_area', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'building_count', 'length', 'natural_area']

obs = []
pred_TW = []
pred_TWA = []
pred_ALL = []
pred_combined = []

for group in range(0,5):
    
    print("Test group " + str(group + 1))
    
    trainStationList = []
    testStationList = []
    for i in range(0,5):
        if i == group:
            testStationList.extend(groups[i])
        else:
            trainStationList.extend(groups[i])

    trainStations = set(float(station) for station in trainStationList)
    
    # reorder train stations
    print("\ttrainStationList:" + str(trainStationList))
    trainStationList = [s for s in all_stations if float(s) in trainStations]
    print("\ttrainStationList:" + str(trainStationList))
    
    testStations = set(float(station) for station in testStationList)
    
    trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TW, "target")
    print("\tTW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    obs.extend(testY)
    pred_TW.extend(prediction)
       
    trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TWA, "target")
    print("\tTWA #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    pred_TWA.extend(prediction)
  
    trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_ALL, "target")
    print("\tALL #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    pred_ALL.extend(prediction)

    trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, columns, "target")

    train_lower = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i < (len(trainStationList) / 2.0)]
    train_upper = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i >= (len(trainStationList) / 2.0)]
    train_lower_set = set(train_lower)
    train_upper_set = set(train_upper)
    
    test_lower = [float(testStationList[i]) for i in range(0, len(testStationList)) if i < (len(testStationList) / 2.0)]
    test_upper = [float(testStationList[i]) for i in range(0, len(testStationList)) if i >= (len(testStationList) / 2.0)]
    
    # lower regression model
    trainX, testX, trainY, testY = splitDataForXValidation(train_lower_set, testStations, "location", data, features_TW, "target")
    print("\tlower TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    test_prediction_lower = model.predict(testX)
    rmse = rmseEval(testY, test_prediction_lower)[1]
    print("\tlower TW rmse: " + str(rmse))

    # lower regression model
    trainX, testX, trainY, testY = splitDataForXValidation(train_upper_set, testStations, "location", data, features_TW, "target")
    print("\tupper TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    test_prediction_upper = model.predict(testX)
    rmse = rmseEval(testY, test_prediction_upper)[1]
    print("\tupper TW rmse: " + str(rmse))
                  
    enabledColumns = [True, True, True, True, True, True, True, True, True, True, True, False, False, True, False, False, True, False]
    all_features = ['hour', 'month', 'day_of_week', 'bank_holiday', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'humidity', 'atc', 'lane_length', 'length', 'building_count', 'building_area', 'leisure_area', 'landuse_area', 'natural_area']
    features = [all_features[i] for i in range(0, len(enabledColumns)) if enabledColumns[i]]
    label_trainX, label_testX, label_trainY, label_testY, label_trainLocation, label_testLocation = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, features, "target")
    
    label_trainY = []
    for l in label_trainLocation:
        if l in train_lower:
            label_trainY.append(0)
        else:
            label_trainY.append(1)
     
    label_testY = []
    for l in label_testLocation:
        if l in test_lower:
            label_testY.append(0)
        else:
            label_testY.append(1)
     
    model = RandomForestClassifier(random_state=42, n_estimators=50, max_depth=4, n_jobs=-1)
    model.fit(label_trainX, label_trainY)
    predY = model.predict(label_testX)
    
    finalPred = []
    for i in range(0, len(predY)):
        if predY[i] == 0:
            finalPred.append(test_prediction_lower[i])
        else:
            finalPred.append(test_prediction_upper[i])
            
    rmse = rmseEval(testY, finalPred)[1]
    print("\tupper+lower TW rmse: " + str(rmse))
    pred_combined.extend(finalPred)

print("FINAL")

rmse = rmseEval(obs, pred_TW)[1]
print("TW rmse: " + str(rmse))
rmse = rmseEval(obs, pred_TWA)[1]
print("TWA rmse: " + str(rmse))
rmse = rmseEval(obs, pred_ALL)[1]
print("ALL rmse: " + str(rmse))
rmse = rmseEval(obs, pred_combined)[1]
print("TW upper+lower rmse: " + str(rmse))
