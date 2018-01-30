from ex29.crossvalidation import splitDataForXValidation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

OUTPUT_FILE = "/experiments/ex29/ex29_4.csv"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_4.txt"
DATA_FILE = "/data/london3_hour_2016.csv"

groups = [['71.0', '70.0', '38.0', '55.0', '91.0', '73.0', '89.0'],
['5.0', '29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0', '13.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0', '51.0']]

all_features = ['building_area', 'building_count', 'natural_area', 'leisure_area', 'landuse_area', 'lane_length', 'length', 'atc', 'windspeed', 'windspeed', 'rain', 'temperature', 'humidity', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday']

output_log = open(OUTPUT_LOG_FILE, "w")
output = open(OUTPUT_FILE, "w")
output.write("min_samples_leaf,n_estimators,rmse\n")

# load the data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

def eval_one(min_samples_leaf, n_estimators):
    log("min_samples_leaf: " + str(min_samples_leaf) + ", n_estimators: " + str(n_estimators))
    
    all_observations = []
    all_pred_ALL = []

    for group in range(0, len(groups)):
        trainStations = []
        for i in range(0, len(groups)):
            if i != group:
                trainStations.extend(groups[i]) 
        testStations = groups[group]
    
        train_station_set = set([float(s) for s in trainStations])
        test_station_set = set([float(s) for s in testStations])
        
        trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, all_features, "target")
        model = RandomForestRegressor(min_samples_leaf = min_samples_leaf, n_estimators = n_estimators, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction_ALL = model.predict(testX)
        rmse = rmseEval(testY, prediction_ALL)[1]
        log("\tALL rmse: " + str(rmse))
        all_observations.extend(testY)
        all_pred_ALL.extend(prediction_ALL)

    rmse = rmseEval(all_observations, all_pred_ALL)[1]
    log("\tALL rmse:" + str(rmse))
    return rmse

for n_estimators in range(50, 1000):
    for min_samples_leaf in range(2,6):
        rmse = eval_one(min_samples_leaf, n_estimators)
        output.write(str(min_samples_leaf))
        output.write(",")
        output.write(str(n_estimators))
        output.write(",")
        output.write(str(rmse))
        output.write("\n")
        output.flush()
        
output_log.close()
output.close()
