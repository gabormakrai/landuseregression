from data.data import loadData
from ex2.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

OUTPUT_LOG_FILE = "/experiments/ex13/ex13_2.txt"

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

all_old_features = ['leisure_area', 'landuse_area', 'buildings_number', 'buildings_area', 'lane_length', 'length', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'traffic_length_car', 'traffic_length_lgv', 'traffic_length_hgv']
log("all_old_features: " + str(all_old_features))

tw_features = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day']
log("tw_features: " + str(tw_features))

twv_features = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'traffic_length_car', 'traffic_length_lgv', 'traffic_length_hgv']
log("twv_features: " + str(twv_features))

twa_features = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'atc']
log("twa_features: " + str(twa_features))

def eval_one(features):
        
    all_predictions = []
    all_observations = []
    
    for location in locations:
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, features, "target")
        model = RandomForestRegressor(min_samples_leaf = 2, random_state=42, n_estimators=650, n_jobs=-1)
        model.fit(trainX, trainY)
        predictions = model.predict(testX)
        all_observations.extend(testY)
        all_predictions.extend(predictions)
    
    rmse = rmseEval(all_observations, all_predictions)[1]
    log("\tRMSE: " + str(rmse))

log("all_old_features")
eval_one(all_old_features)

log("tw_features")
eval_one(tw_features)

log("twv_features")
eval_one(twv_features)

log("twa_features")
eval_one(twa_features)

output_log.close()
