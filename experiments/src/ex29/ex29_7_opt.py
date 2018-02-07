import os.path
from copy import deepcopy
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
import random
from ex29.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationWithLocation

DATA_FILE = "/data/london3_hour_2016.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_7_rmse_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_7_rmse_log.txt"
CACHE_FILE = "/experiments/ex29/ex29_7_cache.csv"

random.seed(42)

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

cached_results = {}

# load cache results
if os.path.isfile(CACHE_FILE):
    with open(CACHE_FILE) as infile:
        for line in infile:
            line = line.rstrip()
            s_line = line.split(";")
            rmse = float(s_line[0])
            l = [s == 'True' for s in s_line[1].split(",")]
            t = tuple(l)
            cached_results[t] = rmse

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
    
    if step in cached_results:
        return cached_results[step]
    
    eval_features = []
    for i in range(0, len(all_features)):
        if step[i]:
            eval_features.append(all_features[i])            
            
    all_observations = []
    all_pred_combined = []

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
        
    rmse = rmseEval(all_observations, all_pred_combined)[1]
    
    cached_results[step] = rmse
    
    # save down the cached result
    
    cache_output = open(CACHE_FILE, "a")
    step_list = [str(s) for s in step]
    step_str = ",".join(step_list)  
    cache_output.write(str(rmse) + ";" + step_str + "\n")
    cache_output.close()
    
    return rmse

best_result = eval_one(tuple(current))
best_step = deepcopy(current)

global_best_result = best_result
global_best_step = deepcopy(best_step)

local_minima_counter = 0
local_minima_limit = 5
local_minima_limit_jumps = 2

for iteration in range(1, 100):

    log("iteration: " + str(iteration))
    log("\tglobal_best_result: " + str(global_best_result))
    log("\tglobal_best_step: " + str(global_best_step))
    log("\tbest_result: " + str(best_result))
    log("\tbest_step: " + str(best_step))
    log("\tcurrent: " + str(current))
    log("\tcurrent_result: " + str(eval_one(tuple(current))))

    output.write(str(iteration))
    output.write(";")
    output.write(str(eval_one(tuple(current))))
    output.write(";")
    output.write(str(current))
    output.write("\n")
    output.flush()

    possible_steps = generate_steps(current)
    possible_steps_result = []

    for step in generate_steps(current):
        step_result = eval_one(tuple(step))
        log("\t\t" + str(step_result) + " <- " + str(step))
        possible_steps_result.append(step_result)

    local_best_result = possible_steps_result[0]
    local_best_step = possible_steps[0]

    for i in range(0, len(possible_steps)):
        if possible_steps_result[i] < local_best_result:
            local_best_result = possible_steps_result[i]
            local_best_step = possible_steps[i]

    log("\tbest local: " + str(local_best_result) + " <- " + str(local_best_step))

    if local_best_result < best_result:
        local_minima_counter = 0
        log("\tFound a better one...")
        best_result = local_best_result
        best_step = local_best_step
        if global_best_result > best_result:
            global_best_result = best_result
            global_best_step = deepcopy(best_step)
        current = best_step
    else:
        local_minima_counter = local_minima_counter + 1
        log("\tLocal minima " + str(local_minima_counter) + "/" + str(local_minima_limit))
        if local_minima_counter < local_minima_limit:
            current = local_best_step
            log("\tCarry on with " + str(local_best_result) + " <- " + str(local_best_step))
        else:
            local_minima_counter = 0
            log("\tQuick random steps:")
            for _ in range(0, local_minima_limit_jumps):
                random_possible_steps = generate_steps(current)
                index = random.randint(0, len(possible_steps) - 1)
                current = random_possible_steps[index]
                log("\t\t" + str(current))
            current_result = eval_one(tuple(current))
            best_result = current_result
            best_step = deepcopy(current)

output.close()
output_log.close()
