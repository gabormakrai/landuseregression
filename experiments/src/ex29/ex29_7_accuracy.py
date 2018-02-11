from copy import deepcopy
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
from ex29.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationWithLocation
from sklearn.metrics.classification import accuracy_score

DATA_FILE = "/data/london3_hour_2016.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_7_accuracy_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_7_accuracy_log.txt"
INPUT_FILE = "/experiments/ex29/ex29_7_rmse_output.csv"
ITERATIONS = 100

stations_in_median_order = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']

groups = [['71.0', '70.0', '38.0', '55.0', '91.0', '73.0', '89.0'],
['5.0', '29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0', '13.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0', '51.0']]

output = open(OUTPUT_FILE, "w")
output_log = open(OUTPUT_LOG_FILE, "w")

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

# load the data
data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

all_features = ['building_area', 'building_count', 'natural_area', 'leisure_area', 'landuse_area', 'lane_length', 'length', 'atc', 'windspeed', 'windspeed', 'rain', 'temperature', 'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
tw_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']

log("all_features: " + str(all_features))
log("tw_features: " + str(tw_features))

current = [True for _ in all_features]

def generate_steps(step):
    next_steps = []

    # generate forward steps
    for i in range(0, len(step)):
        if not step[i]:
            new_step = deepcopy(step)
            new_step[i] = True
            next_steps.append(new_step)

    # generate backwards steps
    for i in range(0, len(step)):
        if step[i]:
            new_step = deepcopy(step)
            new_step[i] = False
            next_steps.append(new_step)

    return next_steps

def create_model():
    return RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)

def create_classifier_model():
    return RandomForestClassifier(max_depth=16, n_estimators = 15, n_jobs = -1, random_state=42)
    
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

def eval_one(step):
        
    eval_features = []
    for i in range(0, len(all_features)):
        if step[i]:
            eval_features.append(all_features[i])            
            
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
        
        trainX, testX, trainY, testY, train_location, test_location = splitDataForXValidationWithLocation(train_station_set, test_station_set, "location", data, eval_features, "target")
        train_label = generate_label(train_location, train_lower)
        test_label = generate_label(test_location, test_lower)
            
        model = create_classifier_model()
        model.fit(trainX, train_label)
        prediction_label = model.predict(testX)
    
        pred_combined = generate_combined_prediction(prediction_label, prediction_lower, prediction_upper)
        all_pred_combined.extend(pred_combined)
        all_observations.extend(testY)
        Y.extend(test_label)
        P.extend(prediction_label)
        
    rmse = rmseEval(all_observations, all_pred_combined)[1]
    accuracy = accuracy_score(Y, P)
        
    return rmse, accuracy

output.write("iteration,rmse,accuracy\n")

rmses = []
steps = []
#1;32.66307423248546;[True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
with open(INPUT_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        s_line = line.split(";")
        rmse = float(s_line[1])
        l = s_line[2][1:len(s_line[2])-1].split(", ")
        step = [x == 'True' for x in l]
        rmses.append(rmse)
        steps.append(step)
        if len(steps) == ITERATIONS:
            break
        
for i in range(0, ITERATIONS):
    log("iteration: " + str(i+1))
    log("\tsaved_rmse: " + str(rmses[i]))
    log("\tstep: " + str(steps[i]))
    rmse, accuracy = eval_one(steps[i])
    log("\tcalculated rmse: " + str(rmse))
    log("\taccuracy: " + str(accuracy))
    output.write(str(i+1) + "," + str(rmse) + "," + str(accuracy) + "\n")

output.close()
output_log.close()
