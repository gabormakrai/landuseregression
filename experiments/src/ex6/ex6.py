from copy import deepcopy
from data.data import loadData
from ex2.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
import random

OUTPUT_FILE = "/experiments/ex6/rmse_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex6/rmse_log.txt"
CACHE_FILE = "/experiments/ex6/ex6_cache.csv"

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
with open("/experiments/ex6/ex6_cache.csv") as infile:
    for line in infile:
        line = line.rstrip()
        s_line = line.split(";")
        rmse = float(s_line[0])
        l = [s == 'True' for s in s_line[1].split(",")]
        t = tuple(l)
        cached_results[t] = rmse

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

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


def eval_one(step):
    
    if step in cached_results:
        return cached_results[step]
    
    eval_features = []
    for i in range(0, len(all_features)):
        if step[i]:
            eval_features.append(all_features[i])
    
    all_predictions = []
    all_observations = []
    
    for location in locations:
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, eval_features, "target")
        model = RandomForestRegressor(min_samples_leaf = 2, random_state=42, n_estimators=650, n_jobs=-1)
        model.fit(trainX, trainY)
        predictions = model.predict(testX)
        all_observations.extend(testY)
        all_predictions.extend(predictions)
    
    rmse = rmseEval(all_observations, all_predictions)[1]
    
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
local_minima_limit = 3
local_minima_limit_jumps = 5

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
    output.write(str(eval_one(current)))
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
        log("\tFound a better one...")
        best_result = local_best_result
        best_step = local_best_step
        if local_best_result < best_result:
            global_best_result = best_result
            global_best_step = deepcopy(best_step)
        current = best_step
    else:
        local_minima_counter = local_minima_counter + 1
        log("\tLocal minima " + str(local_minima_counter) + "/" + str(local_minima_limit))
        if local_minima_counter < local_minima_limit:
            index = random.randint(0, len(possible_steps) - 1)
            current = possible_steps[index]
            current_result = eval_one(current)
            best_result = current_result
            best_step = deepcopy(current)
            log("\tCarry on with " + str(possible_steps_result[index]) + " <- " + str(possible_steps[index]))
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
