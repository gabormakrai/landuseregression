from ex29.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationWithLocation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
from sklearn.metrics.classification import accuracy_score

OUTPUT_LOG_FILE = "/experiments/ex29/ex29_7_opt_classifier.txt"
OUTPUT_FILE = "/experiments/ex29/ex29_7_opt_classifier.csv"
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

enabled_classification_features = [True for _ in all_features]
classification_features = [all_features[i] for i in range(0, len(all_features)) if enabled_classification_features[i]]

def create_model():
    return RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)

def create_classifier_model(max_depth, n_estimators):
    return RandomForestClassifier(max_depth=max_depth, n_estimators = n_estimators, n_jobs = -1, random_state=42)

output_log = open(OUTPUT_LOG_FILE, "w")
output = open(OUTPUT_FILE, "w")
output.write("max_depth,n_estimators,accuracy,rmse\n")

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

def evalOne(max_depth, n_esimators):
    
    all_observations = []
    all_pred_combined = []
    Y = []
    P = []
    
    for group in range(0, len(groups)):
        train_stations, test_stations = generate_train_test_station_list(group, groups)
        train_station_set = set([float(s) for s in train_stations])
        test_station_set = set([float(s) for s in test_stations])
          
        train_lower = [float(train_stations[i]) for i in range(0, len(train_stations)) if i < (len(train_stations) / 2.0)]
        train_lower_set = set(train_lower)
        train_upper = [float(train_stations[i]) for i in range(0, len(train_stations)) if i >= (len(train_stations) / 2.0)]
        train_upper_set = set(train_upper)
        test_lower = [float(test_stations[i]) for i in range(0, len(test_stations)) if i < (len(test_stations) / 2.0)]
            
        # tw_lower
        trainX, testX, trainY, testY = splitDataForXValidation(train_lower_set, test_station_set, "location", data, tw_features, "target")
        model = create_model()
        model.fit(trainX, trainY)
        prediction_lower = model.predict(testX)
        
        # tw_upper
        trainX, testX, trainY, testY = splitDataForXValidation(train_upper_set, test_station_set, "location", data, tw_features, "target")
        model = create_model()
        model.fit(trainX, trainY)
        prediction_upper = model.predict(testX)
            
        trainX, testX, trainY, testY, train_location, test_location = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, classification_features, "target")
        all_observations.extend(testY)
        train_label = generate_label(train_location, train_lower)
        test_label = generate_label(test_location, test_lower)
                
        model = create_classifier_model(max_depth, n_esimators)
        model.fit(trainX, train_label)
        prediction_label = model.predict(testX)
        
        pred_combined = generate_combined_prediction(prediction_label, prediction_lower, prediction_upper)
        all_pred_combined.extend(pred_combined)
        
        Y.extend(test_label)
        P.extend(prediction_label)
        
    accuracy = accuracy_score(Y, P)
    rmse = rmseEval(all_observations, all_pred_combined)[1]
    return accuracy, rmse

for max_depth in range(4,40):
    for n_estimators in [5 * i for i in range(2,20)]:
        accuracy, rmse = evalOne(max_depth, n_estimators)
        log("max_depth: " + str(max_depth) + ", n_estimators: " + str(n_estimators) + ", accuracy: " + str(accuracy) + ", rmse: " + str(rmse))
        output.write(str(max_depth))
        output.write(",")
        output.write(str(n_estimators))
        output.write(",")
        output.write(str(accuracy))
        output.write(",")
        output.write(str(rmse))
        output.write("\n")
        output.flush()

output_log.close()
output.close()
