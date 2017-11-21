from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from ex26.crossvalidation import splitDataForXValidation, splitDataForXValidationWithLocation
from eval.rmse import rmseEval
from ex28.ex28_lib import log

OUTPUT_FILE = "/experiments/ex28/ex28_5_data.csv"
OUTPUT_LOG_FILE = "/experiments/ex28/ex28_5.txt"

all_stations = ['71.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0']

groups = [['71.0', '70.0', '38.0', '55.0', '73.0', '89.0'],
['29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0']]

DATA_FILE = "/data/london3_hour_2016.csv"

steps = [
    [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True],
    [True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False],
    [True, True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, True, False],
    [True, True, True, True, True, True, True, True, True, True, True, False, False, True, False, True, True, False],
    [True, True, True, True, True, True, True, False, True, True, True, False, False, True, False, True, True, False],
    [True, True, True, True, True, False, True, False, True, True, True, False, False, True, False, True, True, False]
]

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

features_TW = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week']
features_TWA = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'atc']
features_ALL = ['leisure_area', 'rain', 'temperature', 'atc', 'windspeed', 'lane_length', 'building_area', 'winddirection', 'landuse_area', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'building_count', 'length', 'natural_area']

obs = []
pred_TW = []
pred_lower = []
pred_upper = []

output = open(OUTPUT_FILE, 'w')
output.write("step,rmse_tw,rmse_lower,rmse_upper,rmse_combined,accuracy\n")

output_log = open(OUTPUT_LOG_FILE, 'w')

log(output_log, "Generating Rmse RFR+TW and Rmse RF+TW lower nd Rmse RFR+TW upper")

for group in range(0,5):
    
    log(output_log, "Test group " + str(group + 1))
    
    trainStationList = []
    testStationList = []
    for i in range(0,5):
        if i == group:
            testStationList.extend(groups[i])
        else:
            trainStationList.extend(groups[i])

    trainStations = set(float(station) for station in trainStationList)
    
    # reorder train stations
    log(output_log, "\ttrainStationList:" + str(trainStationList))
    trainStationList = [s for s in all_stations if float(s) in trainStations]
    log(output_log, "\ttrainStationList:" + str(trainStationList))
    
    testStations = set(float(station) for station in testStationList)
    
    trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TW, "target")
    log(output_log, "\tTW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    log(output_log, "\trmse: " + str(rmse))
    obs.extend(testY)
    pred_TW.extend(prediction)
         
    trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, columns, "target")

    train_lower = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i < (len(trainStationList) / 2.0)]
    train_upper = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i >= (len(trainStationList) / 2.0)]
    train_lower_set = set(train_lower)
    train_upper_set = set(train_upper)
    
    test_lower = [float(testStationList[i]) for i in range(0, len(testStationList)) if i < (len(testStationList) / 2.0)]
    test_upper = [float(testStationList[i]) for i in range(0, len(testStationList)) if i >= (len(testStationList) / 2.0)]
    
    # lower regression model
    trainX, testX, trainY, testY = splitDataForXValidation(train_lower_set, testStations, "location", data, features_TW, "target")
    log(output_log, "\tlower TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    test_prediction_lower = model.predict(testX)
    rmse = rmseEval(testY, test_prediction_lower)[1]
    log(output_log, "\tlower TW rmse: " + str(rmse))
    pred_lower.extend(test_prediction_lower)

    # lower regression model
    trainX, testX, trainY, testY = splitDataForXValidation(train_upper_set, testStations, "location", data, features_TW, "target")
    log(output_log, "\tupper TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    test_prediction_upper = model.predict(testX)
    rmse = rmseEval(testY, test_prediction_upper)[1]
    log(output_log, "\tupper TW rmse: " + str(rmse))
    pred_upper.extend(test_prediction_upper)
                  
rmse_TW = rmseEval(obs, pred_TW)[1]
log(output_log, "TW rmse: " + str(rmse_TW))
rmse_lower = rmseEval(obs, pred_lower)[1]
log(output_log, "TW lower rmse: " + str(rmse_lower))
rmse_upper = rmseEval(obs, pred_upper)[1]
log(output_log, "TW upper rmse: " + str(rmse_upper))

for step in range(0, len(steps)):
    enabledColumns = steps[step]
    log(output_log, "enabledColumns: " + str(enabledColumns))
    pred_combined = []
    
    all_predY = []
    all_labelY = []
    
    for group in range(0,5):
        
        log(output_log, "Test group " + str(group + 1))
        
        trainStationList = []
        testStationList = []
        for i in range(0,5):
            if i == group:
                testStationList.extend(groups[i])
            else:
                trainStationList.extend(groups[i])
    
        trainStations = set(float(station) for station in trainStationList)
        
        # reorder train stations
        log(output_log, "\ttrainStationList:" + str(trainStationList))
        trainStationList = [s for s in all_stations if float(s) in trainStations]
        log(output_log, "\ttrainStationList:" + str(trainStationList))
        
        testStations = set(float(station) for station in testStationList)
                
        log(output_log, "\ttestStationList:" + str(testStationList))
        testStationList = [s for s in all_stations if float(s) in testStations]
        log(output_log, "\ttestStationList:" + str(testStationList))
                     
        trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, columns, "target")
    
        train_lower = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i < (len(trainStationList) / 2.0)]
        train_upper = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i >= (len(trainStationList) / 2.0)]
        train_lower_set = set(train_lower)
        train_upper_set = set(train_upper)
        
        test_lower = [float(testStationList[i]) for i in range(0, len(testStationList)) if i < (len(testStationList) / 2.0)]
        test_upper = [float(testStationList[i]) for i in range(0, len(testStationList)) if i >= (len(testStationList) / 2.0)]
        
        # lower regression model
        trainX, testX, trainY, testY = splitDataForXValidation(train_lower_set, testStations, "location", data, features_TW, "target")
        log(output_log, "\tlower TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        test_prediction_lower = model.predict(testX)
        rmse = rmseEval(testY, test_prediction_lower)[1]
        log(output_log, "\tlower TW rmse: " + str(rmse))
    
        # lower regression model
        trainX, testX, trainY, testY = splitDataForXValidation(train_upper_set, testStations, "location", data, features_TW, "target")
        log(output_log, "\tupper TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        test_prediction_upper = model.predict(testX)
        rmse = rmseEval(testY, test_prediction_upper)[1]
        log(output_log, "\tupper TW rmse: " + str(rmse))
                      
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
          
        model = RandomForestClassifier(random_state=42, n_estimators=30, max_depth=4, n_jobs=-1)
        model.fit(label_trainX, label_trainY)
        predY = model.predict(label_testX)
        
        accuracy = 0
        for i in range(0, len(predY)):
            if predY[i] == label_testY[i]:
                accuracy = accuracy + 1
                
        accuracy = float(accuracy) / float(len(predY))
        log(output_log, "\tupper+lower TW accuraccy: " + str(accuracy))
        
        all_predY.extend(predY)
        all_labelY.extend(label_testY)
         
        finalPred = []
        for i in range(0, len(predY)):
            if predY[i] == 0:
                finalPred.append(test_prediction_lower[i])
            else:
                finalPred.append(test_prediction_upper[i])
                 
        rmse = rmseEval(testY, finalPred)[1]
        log(output_log, "\tupper+lower TW rmse: " + str(rmse))
        pred_combined.extend(finalPred)

    accuracy = 0
    for i in range(0, len(all_predY)):
        if all_predY[i] == all_labelY[i]:
            accuracy = accuracy + 1
            
    accuracy = float(accuracy) / float(len(all_predY))
    log(output_log, "TW combined accuraccy: " + str(accuracy))
        
    rmse_combined = rmseEval(obs, pred_combined)[1]
    log(output_log, "TW combined rmse: " + str(rmse_combined))
    
    output.write(str(step))
    output.write(",")
    output.write(str(rmse_TW))
    output.write(",")
    output.write(str(rmse_lower))
    output.write(",")
    output.write(str(rmse_upper))
    output.write(",")
    output.write(str(rmse_combined))
    output.write(",")
    output.write(str(accuracy))
    output.write("\n")
    output.flush()

output.close()
output_log.close()