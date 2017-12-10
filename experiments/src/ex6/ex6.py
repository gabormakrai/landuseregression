from copy import deepcopy
from data.data import loadData
from ex2.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
import random

OUTPUT_FILE = "/experiments/ex6/rmse_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex6/rmse_log.txt"

output = open(OUTPUT_FILE, "w")
output_log = open(OUTPUT_LOG_FILE, "w")

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

cached_results = {}
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
    
    rmse = rmseEval(all_observations, all_predictions)[0]
    
    return rmse


best_result = eval_one(current)
best_step = deepcopy(current)
cached_results[tuple(current)] = best_result

local_minima_counter = 0
local_minima_limit = 3
local_minima_limit_jumps = 5

for iteration in range(1, 100):

    log("iteration: " + str(iteration))
    log("\tbest_result: " + str(best_result))
    log("\tbest_step: " + str(best_step))
    log("\tcurrent: " + str(current))

    output.write(str(iteration))
    output.write(";")
    output.write(str(best_result))
    output.write(";")
    output.write(str(best_step))
    output.write("\n")
    output.flush()

    possible_steps = generate_steps(current)
    possible_steps_result = []

    for step in generate_steps(current):

        step_tuple = tuple(step)
        if step_tuple in cached_results:
            step_result = cached_results[step_tuple]
        else:
            step_result = eval_one(step)
            cached_results[step_tuple] = step_result
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
        current = best_step
    else:
        local_minima_counter = local_minima_counter + 1
        log("\tLocal minima " + str(local_minima_counter) + "/" + str(local_minima_limit))
        if local_minima_counter < local_minima_limit:
            index = random.randint(0, len(possible_steps) - 1)
            current = possible_steps[index]
            log("\tCarry on with " + str(possible_steps_result[index]) + " <- " + str(possible_steps[index]))
        else:
            local_minima_counter = 0
            for _ in range(0, local_minima_limit_jumps):
                random_possible_steps = generate_steps(current)


output.close()
output_log.close()
