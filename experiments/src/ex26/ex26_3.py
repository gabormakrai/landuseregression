from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from ex26.crossvalidation import splitDataForXValidation, splitDataForXValidation2 
from eval.rmse import rmseEval

# all_stations = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']
all_stations = ['71.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0']

# groups = [['71.0', '70.0', '38.0', '55.0', '91.0', '73.0', '89.0'],
# ['5.0', '29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
# ['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
# ['69.0', '52.0', '26.0', '79.0', '9.0', '16.0', '13.0'],
# ['15.0', '57.0', '24.0', '19.0', '43.0', '33.0', '51.0']]
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

#for group in range(3,4):
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
#      
#     trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TWA, "target")
#     print("\tTWA #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
#     model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
#     model.fit(trainX, trainY)
#     prediction = model.predict(testX)
#     rmse = rmseEval(testY, prediction)[1]
#     print("\trmse: " + str(rmse))
# 
#     trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_ALL, "target")
#     print("\tALL #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
#     model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
#     model.fit(trainX, trainY)
#     prediction = model.predict(testX)
#     rmse = rmseEval(testY, prediction)[1]
#     print("\trmse: " + str(rmse))
#     
#     lower_stations = []
#     upper_stations = []
#     for i in range(0, len(trainStationList)):
#         if i < len(trainStationList) / 2.0:
#             lower_stations.append(trainStationList[i])
#         else:
#             upper_stations.append(trainStationList[i])
#             
#     # lower stations model    
#     print("\tlower_stations: " + str(lower_stations))
#     trainStations = set(float(station) for station in lower_stations)
#     trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TW, "target")
#     print("\tTW lower #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
#     model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
#     model.fit(trainX, trainY)
#     prediction = model.predict(testX)
#     rmse = rmseEval(testY, prediction)[1]
#     print("\trmse: " + str(rmse))
#     
#     # lower stations model    
#     print("\tupper_stations: " + str(upper_stations))
#     trainStations = set(float(station) for station in upper_stations)
#     trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TW, "target")
#     print("\tTW upper #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
#     model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
#     model.fit(trainX, trainY)
#     prediction = model.predict(testX)
#     rmse = rmseEval(testY, prediction)[1]
#     print("\trmse: " + str(rmse))
    
    train_1_stations = []
    train_2_stations = []
    for i in range(0, len(trainStationList)):
        if i % 7 == 0 or i % 7 == 6:#  or i % 7 == 6:
            train_2_stations.append(trainStationList[i])
        else:
            train_1_stations.append(trainStationList[i])
    print("\ttrain_1_stations: " + str(train_1_stations)) 
    print("\ttrain_2_stations: " + str(train_2_stations))

    train2Stations = set([float(s) for s in train_2_stations])
    
    train_1_lower = [float(train_1_stations[i]) for i in range(0, len(train_1_stations)) if i < (len(train_1_stations) / 2.0) - 1]
    train_1_upper = [float(train_1_stations[i]) for i in range(0, len(train_1_stations)) if i >= (len(train_1_stations) / 2.0) + 1]
        
    print("\ttrain_1_lower: " + str(train_1_lower)) 
    print("\ttrain_1_upper: " + str(train_1_upper))
    
    train_2_lower = [float(train_2_stations[i]) for i in range(0, len(train_2_stations)) if i < (len(train_2_stations) / 2.0)]
    train_2_upper = [float(train_2_stations[i]) for i in range(0, len(train_2_stations)) if i >= (len(train_2_stations) / 2.0)]
    
    print("\ttrain_2_lower: " + str(train_2_lower)) 
    print("\ttrain_2_upper: " + str(train_2_upper))
    
    train1LowerSet = set([s for s in train_1_lower]) 
    train1X_L, train2X_L, testX_L, train1Y_L, train2Y_L, testY_L = splitDataForXValidation2(train1LowerSet, train2Stations, testStations, "location", data, features_TW, "target")     
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(train1X_L, train1Y_L)
    train2Prediction_L = model.predict(train2X_L)
    testPrediction_L = model.predict(testX_L)

    train1UpperSet = set([s for s in train_1_upper]) 
    train1X_U, train2X_U, testX_U, train1Y_U, train2Y_U, testY_U = splitDataForXValidation2(train1UpperSet, train2Stations, testStations, "location", data, features_TW, "target")     
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(train1X_U, train1Y_U)
    train2Prediction_U = model.predict(train2X_U)
    testPrediction_U = model.predict(testX_U)

    label = []
#     for i in range(0, len(data["location"])):
#         l = data["location"][i]
#         if l in train_2_lower:
#             label.append(0)
#         elif l in train_2_upper:
#             label.append(1)

    for i in range(0, len(train2Y_L)):
        y = train2Y_L[i]
        p_L = train2Prediction_L[i]
        p_U = train2Prediction_U[i]
        if abs(y - p_L) < abs(y - p_U):
            label.append(0)
        else:
            label.append(1)

    _, train2X, testX, _, _, testY = splitDataForXValidation2(train1UpperSet, train2Stations, testStations, "location", data, features_ALL, "target")
    
    # add train2 preds
    for i in range(0, len(train2X)):
        train2X[i].append(train2Prediction_L[i])
        train2X[i].append(train2Prediction_U[i])
    # add test preds
    for i in range(0, len(testX)):
        testX[i].append(testPrediction_L[i])
        testX[i].append(testPrediction_U[i])

    model = RandomForestClassifier(random_state=42, n_estimators=100, min_samples_leaf=100, n_jobs=-1)
    model.fit(train2X, label)
    testLabelPred = model.predict(testX)
    
    finalPred = []
    used_L = 0
    used_U = 0
    for i in range(0, len(testLabelPred)):
        if testLabelPred[i] == 0:
            finalPred.append(testPrediction_L[i])
            used_L = used_L + 1
        else:
            finalPred.append(testPrediction_U[i])
            used_U = used_U + 1
    
    print("\tused_L: " + str(used_L) + ", used_U: " + str(used_U))
    rmse = rmseEval(testY, finalPred)[1]
    print("\trmse: " + str(rmse))
    