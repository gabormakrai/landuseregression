from data.data import loadData
from collections import defaultdict
from ex21.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

DATA_FILE = "/data/london_hour_2015.csv"

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

dataByStation = defaultdict(lambda: defaultdict(list))

for i in range(0, len(data["location"])):
    loc = data["location"][i]
    for c in columns:
        dataByStation[loc][c].append(data[c][i])

def evalTrainStationTestStation(trainStation, testStation):
    trainX, _, trainY, _ = splitDataForXValidation(set([trainStation]), set(), "location", dataByStation[trainStation], columns, "target")
    _, testX2, _, testY2 = splitDataForXValidation(set(), set([testStation]), "location", dataByStation[testStation], columns, "target")
    model = RandomForestRegressor(max_depth=10, n_estimators = 60, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX2)
    rmse = rmseEval(testY2, prediction)[1]
    print("Training on station " + str(trainStation) + ", applying on station " + str(testStation) + ": rmse: " + str(rmse))

locations = ['61.0', '66.0', '64.0', '25.0', '1.0', '36.0', '4.0', '59.0', '56.0', '3.0', '62.0', '34.0', '77.0', '18.0', '22.0', '71.0', '5.0', '75.0', '10.0', '21.0', '69.0', '60.0', '27.0', '2.0', '41.0', '80.0', '52.0', '47.0', '74.0', '39.0', '58.0', '37.0', '28.0', '63.0', '23.0', '92.0', '38.0', '67.0', '70.0', '31.0', '15.0', '82.0', '29.0', '57.0', '93.0', '87.0', '24.0', '68.0', '86.0', '35.0', '26.0', '12.0', '81.0', '53.0', '20.0', '55.0', '65.0', '6.0', '17.0', '49.0', '54.0', '48.0', '40.0', '79.0', '91.0', '43.0', '76.0', '14.0', '9.0', '78.0', '73.0', '19.0', '32.0', '42.0', '46.0', '30.0', '85.0', '45.0', '50.0', '8.0', '72.0', '33.0', '16.0', '11.0', '88.0', '84.0', '44.0', '7.0', '13.0', '90.0', '83.0', '89.0', '51.0']

for testStation in locations:
    evalTrainStationTestStation(23.0, float(testStation))
