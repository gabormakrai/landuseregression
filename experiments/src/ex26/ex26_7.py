from data.data import loadData
from ex26.crossvalidation import splitDataForXValidationWithLocation
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.metrics.classification import f1_score, accuracy_score
from copy import deepcopy

all_features = ['hour', 'month', 'day_of_week', 'bank_holiday', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'humidity', 'atc', 'lane_length', 'length', 'building_count', 'building_area', 'leisure_area', 'landuse_area', 'natural_area']
all_stations = ['71.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0']

groups = [['71.0', '70.0', '38.0', '55.0', '73.0', '89.0'],
['29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0']]

DATA_FILE = "/data/london3_hour_2016.csv"
OUTPUT_FILE = "/experiments/ex26/ex26_7.txt"

output = open(OUTPUT_FILE, 'w')

def log(message):
    print(message)
    output.write(message)
    output.write("\n")
    output.flush()
    
data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

log("columns: " + str(columns))

def evalOne(enabledColumns):
    features = [all_features[i] for i in range(0, len(all_features)) if enabledColumns[i]]
    Y = []
    P = []
    for group in range(0,5):
    #     print("Test group " + str(group + 1))
        trainStationList = []
        testStationList = []
        for i in range(0,5):
            if i == group:
                testStationList.extend(groups[i])
            else:
                trainStationList.extend(groups[i])
        trainStations = set(float(station) for station in trainStationList)
        # reorder train stations
    #     print("\ttrainStationList:" + str(trainStationList))
        trainStationList = [s for s in all_stations if float(s) in trainStations]
    #     print("\ttrainStationList:" + str(trainStationList))
        testStations = set(float(station) for station in testStationList)
    #     print("\ttestStationList:" + str(testStationList))
        trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, features, "target")
     
        train_lower = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i < (len(trainStationList) / 2.0)]
#         train_upper = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i >= (len(trainStationList) / 2.0)]
         
        test_lower = [float(testStationList[i]) for i in range(0, len(testStationList)) if i < (len(testStationList) / 2.0)]
#         test_upper = [float(testStationList[i]) for i in range(0, len(testStationList)) if i >= (len(testStationList) / 2.0)]
         
        trainY = []
        for l in trainLocation:
            if l in train_lower:
                trainY.append(0)
            else:
                trainY.append(1)
         
        testY = []
        for l in testLocation:
            if l in test_lower:
                testY.append(0)
            else:
                testY.append(1)
         
        model = RandomForestClassifier(random_state=42, n_estimators=20, max_depth=9, n_jobs=-1)
        model.fit(trainX, trainY)
        predY = model.predict(testX)
         
        Y.extend(testY)
        P.extend(predY)
     
    f1 = f1_score(Y, P)
    accuracy = accuracy_score(Y, P)
    return f1, accuracy

def generatePossibleSteps(currentColumns):
    nextSteps = []
    
    l = len(currentColumns)
    enabled = len([1 for c in currentColumns if c])
    if (l != enabled):
        for i in range(0, len(currentColumns)):
            if currentColumns[i]:
                continue
            step = deepcopy(currentColumns)
            step[i] = True
            nextSteps.append(step)
        
    for i in range(0, len(currentColumns)):
        if not currentColumns[i]:
            continue
        step = deepcopy(currentColumns)
        step[i] = False
        nextSteps.append(step)
    
    return nextSteps


log("all_features:" + str(all_features))

currentColumns = [True for c in all_features]
bestSoFarColumns = deepcopy(currentColumns)
bestSoFarAccuracy = 0.0

for iteration in range(0, 1000000):
    log("BestSoFar: " + str(bestSoFarAccuracy) + " <- " + str(bestSoFarColumns))
    
    steps = generatePossibleSteps(currentColumns)
        
    accuracies = []
    for step in steps:
        f1, accuracy = evalOne(step)
        log("\t" + str(accuracy) + ",f1:" + str(f1) + " <- " + str(step))
        accuracies.append(accuracy)
    iterationBest = None
    iterationBestAccuracy = 0.0
    for i in range(0, len(accuracies)):
        if accuracies[i] > iterationBestAccuracy:
            iterationBestAccuracy = accuracies[i]
            iterationBest = steps[i]
    log("iterationBest: " + str(iterationBestAccuracy) + " <- " + str(iterationBest))
    if iterationBestAccuracy > bestSoFarAccuracy:
        bestSoFarAccuracy = iterationBestAccuracy
        bestSoFarColumns = iterationBest
        
    currentColumns = iterationBest

output.close()