from copy import deepcopy
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
import random
from ex27.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationForCombination

OUTPUT_FILE = "/experiments/ex27/rmse_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex27/rmse_log.txt"
CACHE_FILE = "/experiments/ex27/ex27_cache.csv"

random.seed(42)

output = open(OUTPUT_FILE, "w")
output_log = open(OUTPUT_LOG_FILE, "w")

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

cached_results = {}

# load cache results
with open(CACHE_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        s_line = line.split(";")
        rmse = float(s_line[0])
        l = [s == 'True' for s in s_line[1].split(",")]
        t = tuple(l)
        cached_results[t] = rmse

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york3_hour_2013.csv", ["timestamp"], data, columns)

tw_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure']
twa_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc']

all_features = []
all_features.extend(['leisure_area', 'landuse_area'])
all_features.extend(['buildings_number', 'buildings_area'])
all_features.extend(['lane_length', 'length'])
all_features.extend(['traffic_length_car', 'traffic_length_lgv', 'traffic_length_hgv'])
all_features.extend(['winddirection', 'windspeed', 'temperature', 'rain', 'pressure'])
all_features.extend(['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day'])

log("all_features: " + str(all_features))

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
    return RandomForestRegressor(min_samples_leaf = 2, n_estimators = 400, n_jobs = -1, random_state=42)

def create_classifier_model():
    return RandomForestClassifier(max_depth=15, n_estimators = 100, n_jobs = -1, random_state=42)
    
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

def eval_one(step):
    
    if step in cached_results:
        return cached_results[step]
    
    eval_features = []
    for i in range(0, len(all_features)):
        if step[i]:
            eval_features.append(all_features[i])
            
    allObservations = []
    allPredictions = []
    allPredictionsTW = []
    allPredictionsTWA = []
    
    for location in locations:
        location2s = [l for l in locations if l != location]
        
        # tw_4stations
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, tw_features, "target")
        allObservations.extend(testY)
        model = create_model()
        model.fit(trainX, trainY)
        predictionTW = model.predict(testX)
        rmse = rmseEval(testY, predictionTW)[1]
        allPredictionsTW.extend(predictionTW)
    
        # tw_4stations
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, twa_features, "target")
        model = create_model()
        model.fit(trainX, trainY)
        predictionTWA = model.predict(testX)
        rmse = rmseEval(testY, predictionTWA)[1]
        allPredictionsTWA.extend(predictionTWA)
        
        #combination
        classifier_X = []
        classifier_Y = []
        for loc in location2s:
            # tw_3stations
            trainX, testX, trainY, testY = splitDataForXValidationForCombination(loc, location, "location", data, tw_features, "target")
            model = create_model()
            model.fit(trainX, trainY)
            prediction_3station_TW = model.predict(testX)
            # twa_3stations
            trainX, testX, trainY, testY = splitDataForXValidationForCombination(loc, location, "location", data, twa_features, "target")
            model = create_model()
            model.fit(trainX, trainY)
            prediction_3station_TWA = model.predict(testX)
            
            trainX, testX, trainY, testY = splitDataForXValidationForCombination(loc, location, "location", data, eval_features, "target")
            classifier_X.extend(testX)
            label = generate_label(testY, prediction_3station_TW, prediction_3station_TWA)
            classifier_Y.extend(label)
        
        model = create_classifier_model()
        model.fit(classifier_X, classifier_Y)
        _, testX, _, testY = splitDataForXValidation(location, "location", data, eval_features, "target")
        classifier_prediction = model.predict(testX)
        combined_prediction = generate_combined_prediction(classifier_prediction, predictionTW, predictionTWA)
        rmse = rmseEval(testY, combined_prediction)[1]
        allPredictions.extend(combined_prediction)
        
    rmse = rmseEval(allObservations, allPredictions)[1]
    
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
