import os.path
from copy import deepcopy
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
import random
from ex29.crossvalidation import splitDataForXValidation

OUTPUT_FILE = "/experiments/ex29/ex29_6_rmse_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_6_rmse_log.txt"
CACHE_FILE = "/experiments/ex27/ex29_6_cache.csv"

random.seed(42)

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
loadData("/data/york3_hour_2013.csv", ["timestamp"], data, columns)

all_features = ['building_area', 'building_count', 'natural_area', 'leisure_area', 'landuse_area', 'lane_length', 'length', 'atc', 'windspeed', 'windspeed', 'rain', 'temperature', 'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
tw_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
twa_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'atc']

log("all_features: " + str(all_features))
log("tw_features: " + str(tw_features))
log("twa_features: " + str(twa_features))

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
    return RandomForestClassifier(max_depth=20, n_estimators = 100, n_jobs = -1, random_state=42)
    
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
          
        trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, tw_features, "target")
        model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction_TW = model.predict(testX)
        rmse = rmseEval(testY, prediction_TW)[1]
        all_observations.extend(testY)
           
        trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, twa_features, "target")
        model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction_TWA = model.predict(testX)
        rmse = rmseEval(testY, prediction_TWA)[1]
        log("\tTWA rmse: " + str(rmse))
        
        group2s = [groups[i] for i in range(0, len(groups)) if i != group]
        log("group2s: " + str(group2s))
        
        #combination
        classifier_X = []
        classifier_Y = []
        for group2 in range(0, len(group2s)):
            train_stations, test_stations = generate_train_test_station_list(group2, group2s)
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
            
            trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, eval_features, "target")
            classifier_X.extend(testX)
            label = generate_label(testY, prediction_3groups_TW, prediction_3groups_TWA)
            classifier_Y.extend(label)
    
        train_stations, test_stations = generate_train_test_station_list(group, groups)
        train_station_set = set([float(s) for s in train_stations])
        test_station_set = set([float(s) for s in test_stations])
         
        model = create_classifier_model()
        model.fit(classifier_X, classifier_Y)
        _, testX, _, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, eval_features, "target")
    
        classifier_prediction = model.predict(testX)
        combined_prediction = generate_combined_prediction(classifier_prediction, prediction_TW, prediction_TWA)
        rmse = rmseEval(testY, combined_prediction)[1]
        log("\tTW+TWA:" + str(rmse))
        all_pred_combined.extend(combined_prediction)    
        
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

for iteration in range(1, 300):

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
