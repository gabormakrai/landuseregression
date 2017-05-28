from ex22.crossvalidation import splitDataForXValidation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

locations = ['71.0', '5.0', '69.0', '52.0', '38.0', '67.0', '70.0', '15.0', '29.0', '57.0', '24.0', '86.0', '81.0', '20.0', '55.0', '79.0', '91.0', '78.0', '9.0', '73.0', '32.0', '19.0', '46.0', '85.0', '50.0', '33.0', '88.0', '44.0', '13.0', '90.0', '89.0', '51.0']

print(str(locations))

print("#locations: " + str(len(locations)))

locations_grouped = [[], [], [], [], []]
for i in range(0, 30):
    group = i % 5
    locations_grouped[group].append(float(locations[i]))
    
for i in range(0, 5):
    print("group_" + str(i) + ": " + str(locations_grouped[i]))
    
DATA_FILE = "/data/london3_hour_2015.csv"

data = {}
columns = []
loadData(DATA_FILE, ["timestamp", 'natural_area','building_count','leisure_area','landuse_area','lane_length','length','building_area'], data, columns)

for iteration in range(0, 5):
    print("iter_" + str(iteration))
    trainStations = []
    testStations = []
    for i in range(0, 5):
        if i == iteration:
            testStations = testStations + locations_grouped[i]
        else:
            trainStations = trainStations + locations_grouped[i]
    print("\ttrainStations: " + str(trainStations))
    print("\ttestStations: " + str(testStations))
    
    trainStationSet = set(s for s in trainStations)
    testStationSet = set(s for s in testStations)
    
    trainX, testX, trainY, testY = splitDataForXValidation(trainStationSet, testStationSet, "location", data, columns, "target")
    print("\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
