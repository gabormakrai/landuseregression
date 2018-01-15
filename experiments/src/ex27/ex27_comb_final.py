from eval.rmse import rmseEval
from sklearn.ensemble.forest import RandomForestClassifier, RandomForestRegressor
from data.data import loadData
from ex27.crossvalidation import splitDataForXValidation, splitDataForXValidationForCombination

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_FILE = "/experiments/ex27/ex27_comb_final.txt"

data = {}
columns = []
loadData(DATA_FILE, ['timestamp'], data, columns)

output = open(OUTPUT_FILE, 'w')

def create_model():
    return RandomForestRegressor(min_samples_leaf = 2, n_estimators = 200, n_jobs = -1, random_state=42)

def create_classifier_model():
    return RandomForestClassifier(max_depth=15, n_estimators = 100, n_jobs = -1, random_state=42)

def log(message):
    print(message)
    output.write(message)
    output.write("\n")
    output.flush()

enabled_features = [False, False, False, False, True, False, False, False, False, True, False, False, True, True, True, False, False, True, False]
all_features = []
all_features.extend(['leisure_area', 'landuse_area'])
all_features.extend(['buildings_number', 'buildings_area'])
all_features.extend(['lane_length', 'length'])
all_features.extend(['traffic_length_car', 'traffic_length_lgv', 'traffic_length_hgv'])
all_features.extend(['winddirection', 'windspeed', 'temperature', 'rain', 'pressure'])
all_features.extend(['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day'])

features = [all_features[i] for i in range(0, len(all_features)) if enabled_features[i]]
log("features: " + str(features))

tw_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure']
twa_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc']

locations = [2.0, 3.0, 4.0, 6.0, 8.0]
    
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

allObservations = []
allPredictions = []
allPredictionsTW = []
allPredictionsTWA = []

for location in locations:
    location2s = [l for l in locations if l != location]
    
    log("Location: " + str(location) + ", location2: " + str(location2s))
    
    # tw_4stations
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, tw_features, "target")
    allObservations.extend(testY)
    model = create_model()
    model.fit(trainX, trainY)
    predictionTW = model.predict(testX)
    rmse = rmseEval(testY, predictionTW)[1]
    log("\tTW:" + str(rmse))
    allPredictionsTW.extend(predictionTW)

    # tw_4stations
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, twa_features, "target")
    model = create_model()
    model.fit(trainX, trainY)
    predictionTWA = model.predict(testX)
    rmse = rmseEval(testY, predictionTWA)[1]
    log("\tTWA:" + str(rmse))
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
        
        trainX, testX, trainY, testY = splitDataForXValidationForCombination(loc, location, "location", data, features, "target")
        classifier_X.extend(testX)
        label = generate_label(testY, prediction_3station_TW, prediction_3station_TWA)
        classifier_Y.extend(label)
    
    model = create_classifier_model()
    model.fit(classifier_X, classifier_Y)
    _, testX, _, testY = splitDataForXValidation(location, "location", data, features, "target")
    classifier_prediction = model.predict(testX)
    combined_prediction = generate_combined_prediction(classifier_prediction, predictionTW, predictionTWA)
    rmse = rmseEval(testY, combined_prediction)[1]
    log("\tTW+TWA:" + str(rmse))
    allPredictions.extend(combined_prediction)

rmse = rmseEval(allObservations, allPredictionsTW)[1]
log("TW: " + str(rmse))
rmse = rmseEval(allObservations, allPredictionsTWA)[1]
log("TWA: " + str(rmse))
rmse = rmseEval(allObservations, allPredictions)[1]
log("TW+TWA: " + str(rmse))
    
output.close()
