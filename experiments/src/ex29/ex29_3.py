from ex29.crossvalidation import splitDataForXValidation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

OUTPUT_LOG_FILE = "/experiments/ex29/ex29_3.txt"
DATA_FILE = "/data/london3_hour_2016.csv"

groups = [['71.0', '70.0', '38.0', '55.0', '91.0', '73.0', '89.0'],
['5.0', '29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0', '13.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0', '51.0']]

all_features = ['building_area', 'building_count', 'natural_area', 'leisure_area', 'landuse_area', 'lane_length', 'length', 'atc', 'windspeed', 'windspeed', 'rain', 'temperature', 'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']

tw_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']
twa_features = ['winddirection', 'windspeed', 'rain', 'temperature',  'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'atc']

output_log = open(OUTPUT_LOG_FILE, "w")

# load the data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)


def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

all_observations = []
all_pred_TW = []
all_pred_TWA = []
all_pred_ALL = []

for group in range(0, len(groups)):
    log("group: " + str(group + 1))
    trainStations = []
    for i in range(0, len(groups)):
        if i != group:
            trainStations.extend(groups[i]) 
    testStations = groups[group]
    log("\ttrainStations: " + str(trainStations))
    log("\ttestStations: " + str(testStations))
    
    train_station_set = set([float(s) for s in trainStations])
    test_station_set = set([float(s) for s in testStations])
    
    trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, tw_features, "target")
    model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction_TW = model.predict(testX)
    rmse = rmseEval(testY, prediction_TW)[1]
    log("\tTW rmse: " + str(rmse))
    all_observations.extend(testY)
    all_pred_TW.extend(prediction_TW)
     
    trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, twa_features, "target")
    model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction_TWA = model.predict(testX)
    rmse = rmseEval(testY, prediction_TWA)[1]
    log("\tTWA rmse: " + str(rmse))
    all_pred_TWA.extend(prediction_TWA)
    
    trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, all_features, "target")
    model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction_ALL = model.predict(testX)
    rmse = rmseEval(testY, prediction_ALL)[1]
    log("\tALL rmse: " + str(rmse))
    all_pred_ALL.extend(prediction_ALL)

rmse = rmseEval(all_observations, all_pred_TW)[1]
log("TW rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_TWA)[1]
log("TWA rmse:" + str(rmse))
rmse = rmseEval(all_observations, all_pred_ALL)[1]
log("ALL rmse:" + str(rmse))

output_log.close()
