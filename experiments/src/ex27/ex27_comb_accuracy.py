from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
from ex27.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationForCombination

ITERATIONS = 30

INPUT_FILE = "/experiments/ex27/rmse_output.csv"
OUTPUT_FILE = "/experiments/ex27/accuracy_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex27/ex27_accuracy.txt"

output = open(OUTPUT_FILE, "w")
output_log = open(OUTPUT_LOG_FILE, "w")

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

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

def calculate_accuracy(obs, pred):
    accuracy = 0
    for i in range(0, len(obs)):
        if obs[i] == pred[i]:
            accuracy = accuracy + 1
    return float(accuracy) / float(len(obs))

def eval_one(step):
        
    eval_features = []
    for i in range(0, len(all_features)):
        if step[i]:
            eval_features.append(all_features[i])
            
    allObservations = []
    allPredictions = []
    allPredictionsTW = []
    allPredictionsTWA = []
    allLabel = []
    allLabelPrediction = []
    
    for location in locations:
        location2s = [l for l in locations if l != location]
        
        # tw_4stations
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, tw_features, "target")
        allObservations.extend(testY)
        model = create_model()
        model.fit(trainX, trainY)
        predictionTW = model.predict(testX)
        allPredictionsTW.extend(predictionTW)
    
        # tw_4stations
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, twa_features, "target")
        model = create_model()
        model.fit(trainX, trainY)
        predictionTWA = model.predict(testX)
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
        classifier_testLabel = generate_label(testY, predictionTW, predictionTWA)
        allLabel.extend(classifier_testLabel)
        allLabelPrediction.extend(classifier_prediction)
        combined_prediction = generate_combined_prediction(classifier_prediction, predictionTW, predictionTWA)
        allPredictions.extend(combined_prediction)
        
    rmse = rmseEval(allObservations, allPredictions)[1]
    accuracy = calculate_accuracy(allLabel, allLabelPrediction)
        
    return rmse, accuracy

output.write("iteration,rmse,accuracy\n")

rmses = []
steps = []
#1;13.092898393942114;[True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
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
