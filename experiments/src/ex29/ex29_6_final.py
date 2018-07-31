from ex29.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationWithLocation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval

OUTPUT_FILE = "/experiments/ex29/ex29_6_final.csv"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_6_final.txt"
DATA_FILE = "/data/london3_hour_2016.csv"

groups = [['71.0', '70.0', '38.0', '55.0', '91.0', '73.0', '89.0'],
['5.0', '29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0', '13.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0', '51.0']]

all_features = ['building_area', 'building_count', 'natural_area', 'leisure_area', 'landuse_area', 'lane_length', 'length', 'atc', 'windspeed', 'windspeed', 'rain', 'temperature', 'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
tw_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
twa_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'atc']

enabled_classification_features = [False, False, True, True, True, False, True, True, False, False, False, False, False, True, True, False, False, True]

def create_model():
    return RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)

def create_classifier_model():
    return RandomForestClassifier(max_depth=20, n_estimators = 100, n_jobs = -1, random_state=42)

output_log = open(OUTPUT_LOG_FILE, "w")
output = open(OUTPUT_FILE, "w")
output.write("prediction,observation,station,model\n")

# load the data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

log("all_features: " + str(all_features))
log("tw_features: " + str(tw_features))
log("twa_features: " + str(twa_features))

classification_features = [all_features[i] for i in range(0, len(all_features)) if enabled_classification_features[i]]
log("classification_features: " + str(classification_features))
    
def generate_label(observations, tw_predictions, twa_predictions):
    label = []
    for i in range(0, len(observations)):
        tw_abs = abs(observations[i] - tw_predictions[i])
        twa_abs = abs(observations[i] - twa_predictions[i])
        if tw_abs < twa_abs:
            label.append(0)
        else:
            label.append(1)
    return label

def generate_combined_prediction(classifier_prediction, prediction_tw, prediction_twa):
    pred = []
    for i in range(0, len(classifier_prediction)):
        if classifier_prediction[i] == 0:
            pred.append(prediction_tw[i])
        else:
            pred.append(prediction_twa[i])
    return pred

def generate_train_test_station_list(group, groups):
    train_stations = []
    for i in range(0, len(groups)):
        if i != group:
            train_stations.extend(groups[i]) 
    test_stations = groups[group]
    return train_stations, test_stations
    
all_observations = []
all_pred_ALL = []
all_pred_TW = []
all_pred_TWA = []
all_pred_combined = []
all_test_location = []

for group in range(0, len(groups)):
    log("group: " + str(group + 1))
        
    train_stations, test_stations = generate_train_test_station_list(group, groups)
    log("\ttrain_stations: " + str(train_stations))
    log("\ttest_stations: " + str(test_stations))
    train_station_set = set([float(s) for s in train_stations])
    test_station_set = set([float(s) for s in test_stations])
    
    trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, all_features, "target")
    model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction_TW = model.predict(testX)
    rmse = rmseEval(testY, prediction_TW)[1]
    log("\tALL rmse: " + str(rmse))
    all_observations.extend(testY)
    all_pred_ALL.extend(prediction_TW)
    all_test_location.extend(testLocation)
      
    trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, tw_features, "target")
    model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction_TW = model.predict(testX)
    rmse = rmseEval(testY, prediction_TW)[1]
    log("\tTW rmse: " + str(rmse))
    all_pred_TW.extend(prediction_TW)
       
    trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, twa_features, "target")
    model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction_TWA = model.predict(testX)
    rmse = rmseEval(testY, prediction_TWA)[1]
    log("\tTWA rmse: " + str(rmse))
    all_pred_TWA.extend(prediction_TWA)
    
    group2s = [groups[i] for i in range(0, len(groups)) if i != group]
    log("group2s: " + str(group2s))
    
    #combination
    classifier_X = []
    classifier_Y = []
    for group2 in range(0, len(group2s)):
        
        train_stations, test_stations = generate_train_test_station_list(group2, group2s)
        log("\ttrain_stations: " + str(train_stations))
        log("\ttest_stations: " + str(test_stations))
        train_station_set = set([float(s) for s in train_stations])
        test_station_set = set([float(s) for s in test_stations])
        
        trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, tw_features, "target")
        model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction_3groups_TW = model.predict(testX)
           
        trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, twa_features, "target")
        model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction_3groups_TWA = model.predict(testX)
        
        trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, classification_features, "target")
        classifier_X.extend(testX)
        label = generate_label(testY, prediction_3groups_TW, prediction_3groups_TWA)
        classifier_Y.extend(label)

    train_stations, test_stations = generate_train_test_station_list(group, groups)
    log("\ttrain_stations: " + str(train_stations))
    log("\ttest_stations: " + str(test_stations))
    train_station_set = set([float(s) for s in train_stations])
    test_station_set = set([float(s) for s in test_stations])
     
    model = create_classifier_model()
    model.fit(classifier_X, classifier_Y)
    _, testX, _, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, classification_features, "target")

    classifier_prediction = model.predict(testX)
    combined_prediction = generate_combined_prediction(classifier_prediction, prediction_TW, prediction_TWA)
    rmse = rmseEval(testY, combined_prediction)[1]
    log("\tTW+TWA:" + str(rmse))
    all_pred_combined.extend(combined_prediction)    
    
rmse = rmseEval(all_observations, all_pred_ALL)[1]
log("ALL rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_TW)[1]
log("TW rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_TWA)[1]
log("TWA rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_combined)[1]
log("TW+TWA rmse:" + str(rmse))

for i in range(0, len(all_observations)):
    obs = all_observations[i]
    pred_ALL = all_pred_ALL[i]
    pred_TW = all_pred_TW[i]
    pred_TWA = all_pred_TWA[i]
    pred_combined = all_pred_combined[i]
    location = all_test_location[i]
    output.write(str(obs) + "," + str(pred_ALL) + ",RFR_ALL," + str(location) + "\n")
    output.write(str(obs) + "," + str(pred_TW) + ",RFR_TW," + str(location) + "\n")
    output.write(str(obs) + "," + str(pred_TWA) + ",RFR_TWA," + str(location) + "\n")
    output.write(str(obs) + "," + str(pred_combined) + ",RFR_combined," + str(location) + "\n")
    
output_log.close()
output.close()
