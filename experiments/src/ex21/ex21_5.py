from ex21.crossvalidation import splitDataForXValidation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

locations = ['61.0', '66.0', '64.0', '25.0', '1.0', '36.0', '4.0', '59.0', '56.0', '3.0', '62.0', '34.0', '77.0', '18.0', '22.0', '71.0', '5.0', '75.0', '10.0', '21.0', '69.0', '60.0', '27.0', '2.0', '41.0', '80.0', '52.0', '47.0', '74.0', '39.0', '58.0', '37.0', '28.0', '63.0', '23.0', '92.0', '38.0', '67.0', '70.0', '31.0', '15.0', '82.0', '29.0', '57.0', '93.0', '87.0', '24.0', '68.0', '86.0', '35.0', '26.0', '12.0', '81.0', '53.0', '20.0', '55.0', '65.0', '6.0', '17.0', '49.0', '54.0', '48.0', '40.0', '79.0', '91.0', '43.0', '76.0', '14.0', '9.0', '78.0', '73.0', '19.0', '32.0', '42.0', '46.0', '30.0', '85.0', '45.0', '50.0', '8.0', '72.0', '33.0', '16.0', '11.0', '88.0', '84.0', '44.0', '7.0', '13.0', '90.0', '83.0', '89.0', '51.0']

print(str(locations))

print("#locations: " + str(len(locations)))

locations_grouped = [[], [], [], [], []]
for i in range(0, 90):
    group = i % 5
    locations_grouped[group].append(float(locations[i]))
    
for i in range(0, 5):
    print("group_" + str(i) + ": " + str(locations_grouped[i]))
    
DATA_FILE = "/data/london_hour_2015.csv"

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
