from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor,\
    RandomForestClassifier
from eval.rmse import rmseEval
from ex29.crossvalidation import splitDataForXValidation

DATA_FILE = "/data/london3_hour_2016.csv"
INPUT_FILE = "/experiments/ex29/ex29_6_rmse_output.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_6_accuracy_output.csv"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_6_accuracy_log.txt"
ITERATIONS = 100

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
twa_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'atc']

log("all_features: " + str(all_features))
log("tw_features: " + str(tw_features))
log("twa_features: " + str(twa_features))

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
            
    all_observations = []
    all_pred_combined = []
    
    all_label = []
    all_pred_label = []
    
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
        
        group2s = [groups[i] for i in range(0, len(groups)) if i != group]
        
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
        test_label = generate_label(testY, prediction_TW, prediction_TWA)
        all_label.extend(test_label)
        all_pred_label.extend(classifier_prediction)
        combined_prediction = generate_combined_prediction(classifier_prediction, prediction_TW, prediction_TWA)
        rmse = rmseEval(testY, combined_prediction)[1]
        all_pred_combined.extend(combined_prediction)    
        
    rmse = rmseEval(all_observations, all_pred_combined)[1]
    accuracy = calculate_accuracy(all_label, all_pred_label)
        
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
