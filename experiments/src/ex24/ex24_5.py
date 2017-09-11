from data.data import loadData
from collections import defaultdict
from ex24.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

DATA_FILE = "/data/london3_hour_2016.csv"
OUTPUT_FILE_TW = "/experiments/ex24/ex25_5_tw.csv"
OUTPUT_FILE_TWA = "/experiments/ex24/ex25_5_twa.csv"
OUTPUT_FILE_ALL = "/experiments/ex24/ex25_5_all.csv"

features_TW = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week']
features_TWA = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'atc']
features_ALL = ['leisure_area', 'rain', 'temperature', 'atc', 'windspeed', 'lane_length', 'building_area', 'winddirection', 'landuse_area', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'building_count', 'length', 'natural_area']

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

dataByStation = defaultdict(lambda: defaultdict(list))

for i in range(0, len(data["location"])):
    loc = data["location"][i]
    for c in columns:
        dataByStation[loc][c].append(data[c][i])

def evalTrainStationTestStation(trainStation, testStation, features):
    trainX, _, trainY, _ = splitDataForXValidation(set([trainStation]), set(), "location", dataByStation[trainStation], features, "target")
    _, testX2, _, testY2 = splitDataForXValidation(set(), set([testStation]), "location", dataByStation[testStation], features, "target")
    model = RandomForestRegressor(max_depth=10, n_estimators = 60, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX2)
    rmse = rmseEval(testY2, prediction)[1]
    print("Training on station " + str(trainStation) + ", applying on station " + str(testStation) + ": rmse: " + str(rmse))
    return rmse

locations = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']

output_tw = open(OUTPUT_FILE_TW, 'w')
output_twa = open(OUTPUT_FILE_TWA, 'w')
output_all = open(OUTPUT_FILE_ALL, 'w')

output_tw.write("train_station,test_station,RMSE\n")
output_twa.write("train_station,test_station,RMSE\n")
output_all.write("train_station,test_station,RMSE\n")

for trainStation in locations:
    for testStation in locations:
        rmse = evalTrainStationTestStation(float(trainStation), float(testStation), features_TW)
        output_tw.write(trainStation + "," + testStation + "," + str(rmse) + "\n")
        output_tw.flush()
        rmse = evalTrainStationTestStation(float(trainStation), float(testStation), features_TWA)
        output_twa.write(trainStation + "," + testStation + "," + str(rmse) + "\n")
        output_twa.flush()
        rmse = evalTrainStationTestStation(float(trainStation), float(testStation), features_ALL)
        output_all.write(trainStation + "," + testStation + "," + str(rmse) + "\n")
        output_all.flush()

output_tw.close()
output_twa.close()
output_all.close()
