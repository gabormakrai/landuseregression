from ex29.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationWithLocation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
from sklearn.metrics.classification import accuracy_score
import time

OUTPUT_LOG_FILE = "/experiments/ex29/ex29_7_time.txt"
DATA_FILE = "/data/london3_hour_2016.csv"

stations_in_median_order = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']

groups = [['71.0', '70.0', '38.0', '55.0', '91.0', '73.0', '89.0'],
['5.0', '29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0', '13.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0', '51.0']]

all_features = ['building_area', 'building_count', 'natural_area', 'leisure_area', 'landuse_area', 'lane_length', 'length', 'atc', 'windspeed', 'windspeed', 'rain', 'temperature', 'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
tw_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
twa_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'atc']

enabled_classification_features = [True, False, True, True, True, True, False, False, True, True, True, True, True, True, True, False, True, True]
classification_features = [all_features[i] for i in range(0, len(all_features)) if enabled_classification_features[i]]

def create_model():
    return RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)

def create_classifier_model():
    return RandomForestClassifier(max_depth=16, n_estimators = 15, n_jobs = -1, random_state=42)

output_log = open(OUTPUT_LOG_FILE, "w")

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
log("stations_in_median_order: " + str(stations_in_median_order))

classification_features = [all_features[i] for i in range(0, len(all_features)) if enabled_classification_features[i]]
log("classification_features: " + str(classification_features))

def generate_label(locations, locations_set):
    label = []
    for l in locations:
        if l in locations_set:
            label.append(0)
        else:
            label.append(1)
    return label
    
def generate_combined_prediction(classifier_prediction, prediction_lower, prediction_upper):
    pred = []
    for i in range(0, len(classifier_prediction)):
        if classifier_prediction[i] == 0:
            pred.append(prediction_lower[i])
        else:
            pred.append(prediction_upper[i])
    return pred

def generate_train_test_station_list(group, groups):
    train_stations = []
    for i in range(0, len(groups)):
        if i != group:
            train_stations.extend(groups[i]) 
    test_stations = groups[group]
    return train_stations, test_stations
    
all_observations = []
all_pred_TW = []
all_pred_TWA = []
all_pred_ALL = []
all_pred_lower = []
all_pred_upper = []
all_pred_combined = []
all_test_location = []

Y = []
P = []

times = []
times_TW = []
times_TWA = []

for group in range(0, len(groups)):
    log("group: " + str(group + 1))
        
    train_stations, test_stations = generate_train_test_station_list(group, groups)
    log("\ttrain_stations: " + str(train_stations))
    log("\ttest_stations: " + str(test_stations))
    train_station_set = set([float(s) for s in train_stations])
    test_station_set = set([float(s) for s in test_stations])
      
    trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, all_features, "target")
    model = create_model()
    model.fit(trainX, trainY)
    prediction_ALL = model.predict(testX)
    rmse = rmseEval(testY, prediction_ALL)[1]
    log("\tALL rmse: " + str(rmse))
    all_observations.extend(testY)
    all_pred_ALL.extend(prediction_ALL)
    all_test_location.extend(testLocation)

    start_time = time.time()
    trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, tw_features, "target")
    model = create_model()
    model.fit(trainX, trainY)
    prediction_TW = model.predict(testX)
    rmse = rmseEval(testY, prediction_TW)[1]
    log("\tTW rmse: " + str(rmse))
    all_pred_TW.extend(prediction_TW)
    times_TW.append(time.time() - start_time)
     
    start_time = time.time()
    trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, twa_features, "target")
    model = create_model()
    model.fit(trainX, trainY)
    prediction_TWA = model.predict(testX)
    rmse = rmseEval(testY, prediction_TWA)[1]
    log("\tTWA rmse: " + str(rmse))
    all_pred_TWA.extend(prediction_TWA)
    times_TWA.append(time.time() - start_time)

    start_time = time.time()

    train_lower = [float(train_stations[i]) for i in range(0, len(train_stations)) if i < (len(train_stations) / 2.0)]
    train_lower_set = set(train_lower)
    train_upper = [float(train_stations[i]) for i in range(0, len(train_stations)) if i >= (len(train_stations) / 2.0)]
    train_upper_set = set(train_upper)
    test_lower = [float(test_stations[i]) for i in range(0, len(test_stations)) if i < (len(test_stations) / 2.0)]
    
    log("\ttrain_lower: " + str(train_lower))
    log("\ttrain_upper: " + str(train_upper))
    
    # tw_lower
    trainX, testX, trainY, testY = splitDataForXValidation(train_lower_set, test_station_set, "location", data, tw_features, "target")
    model = create_model()
    model.fit(trainX, trainY)
    prediction_lower = model.predict(testX)
    rmse = rmseEval(testY, prediction_lower)[1]
    log("\tTW_lower rmse: " + str(rmse))
    all_pred_lower.extend(prediction_lower)
    
    # tw_upper
    trainX, testX, trainY, testY = splitDataForXValidation(train_upper_set, test_station_set, "location", data, tw_features, "target")
    model = create_model()
    model.fit(trainX, trainY)
    prediction_upper = model.predict(testX)
    rmse = rmseEval(testY, prediction_upper)[1]
    log("\tTW_upper rmse: " + str(rmse))
    all_pred_upper.extend(prediction_upper)
        
    trainX, testX, trainY, testY, train_location, test_location = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, classification_features, "target")
    train_label = generate_label(train_location, train_lower)
    test_label = generate_label(test_location, test_lower)
            
    model = create_classifier_model()
    model.fit(trainX, train_label)
    prediction_label = model.predict(testX)
    accuracy = accuracy_score(test_label, prediction_label)
    log("\taccuracy: " + str(accuracy))
    
    Y.extend(test_label)
    P.extend(prediction_label)
    
    pred_combined = generate_combined_prediction(prediction_label, prediction_lower, prediction_upper)
    rmse = rmseEval(testY, pred_combined)[1]
    log("\tTW_combined rmse: " + str(rmse))
    all_pred_combined.extend(pred_combined)
    times.append(time.time() - start_time)
    
    
log("Overall result:")
    
rmse = rmseEval(all_observations, all_pred_TW)[1]
log("TW rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_TWA)[1]
log("TWA rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_ALL)[1]
log("ALL rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_lower)[1]
log("TW_lower:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_upper)[1]
log("TW_upper:" + str(rmse))

accuracy = accuracy_score(Y, P)
log("combined accuracy: " + str(accuracy))    
rmse = rmseEval(all_observations, all_pred_combined)[1]
log("combined rmse:" + str(rmse))

log("timesTW: " + str(times_TW))
log("sum(timesTW): " + str(sum(times_TW)))
log("timesTWA: " + str(times_TWA))
log("sum(timesTWA): " + str(sum(times_TWA)))
log("times: " + str(times))
log("sum(times): " + str(sum(times)))
    
output_log.close()
