from data.data import loadData
from ex26.crossvalidation import splitDataForXValidationWithLocation
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.metrics.classification import f1_score, confusion_matrix,\
    accuracy_score

all_stations = ['71.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0']

groups = [['71.0', '70.0', '38.0', '55.0', '73.0', '89.0'],
['29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0']]

DATA_FILE = "/data/london3_hour_2016.csv"

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

Y = []
P = []
P2 = []
P3 = []
P4 = []

for group in range(0,5):
    
    print("Test group " + str(group + 1))
    
    trainStationList = []
    testStationList = []
    for i in range(0,5):
        if i == group:
            testStationList.extend(groups[i])
        else:
            trainStationList.extend(groups[i])

    trainStations = set(float(station) for station in trainStationList)
    
    # reorder train stations
    print("\ttrainStationList:" + str(trainStationList))
    trainStationList = [s for s in all_stations if float(s) in trainStations]
    print("\ttrainStationList:" + str(trainStationList))
    
    testStations = set(float(station) for station in testStationList)
    print("\ttestStationList:" + str(testStationList))

    trainX, testX, trainY, testY, trainLocation, testLocation = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, columns, "target")

    train_lower = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i < (len(trainStationList) / 2.0)]
    train_upper = [float(trainStationList[i]) for i in range(0, len(trainStationList)) if i >= (len(trainStationList) / 2.0)]
    
    test_lower = [float(testStationList[i]) for i in range(0, len(testStationList)) if i < (len(testStationList) / 2.0)]
    test_upper = [float(testStationList[i]) for i in range(0, len(testStationList)) if i >= (len(testStationList) / 2.0)]
    
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
    
    model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=8, n_jobs=-1)
    model.fit(trainX, trainY)
    predY = model.predict(testX)
    
    Y.extend(testY)
    P.extend(predY)

    model = RandomForestClassifier(random_state=42, n_estimators=30, max_depth=4, n_jobs=-1)
    model.fit(trainX, trainY)
    predY = model.predict(testX)
    P2.extend(predY)
    
    enabledColumns = [True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False]
    all_features = ['hour', 'month', 'day_of_week', 'bank_holiday', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'humidity', 'atc', 'lane_length', 'length', 'building_count', 'building_area', 'leisure_area', 'landuse_area', 'natural_area']
    features = [all_features[i] for i in range(0, len(enabledColumns)) if enabledColumns[i]]
    trainX, testX, _, _, _, _ = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, features, "target")
    
    model = RandomForestClassifier(random_state=42, n_estimators=30, max_depth=4, n_jobs=-1)
    model.fit(trainX, trainY)
    predY = model.predict(testX)
    P3.extend(predY)
    
    enabledColumns = [True, True, True, True, True, False, True, False, True, True, True, False, False, True, False, True, True, False]
    all_features = ['hour', 'month', 'day_of_week', 'bank_holiday', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'humidity', 'atc', 'lane_length', 'length', 'building_count', 'building_area', 'leisure_area', 'landuse_area', 'natural_area']
    features = [all_features[i] for i in range(0, len(enabledColumns)) if enabledColumns[i]]
    trainX, testX, _, _, _, _ = splitDataForXValidationWithLocation(trainStations, testStations, "location", data, features, "target")
    
    model = RandomForestClassifier(random_state=42, n_estimators=30, max_depth=4, n_jobs=-1)
    model.fit(trainX, trainY)
    predY = model.predict(testX)
    P4.extend(predY)
    
print("M1:")
m = confusion_matrix(Y, P)
print("Confusion matrix:")
print(str(m))
f1 = f1_score(Y, P)
print("f1_score:")
print(str(f1))
accuracy = accuracy_score(Y, P)
print("accuracy:")
print(str(accuracy))
    
print("M2:")
m = confusion_matrix(Y, P2)
print("Confusion matrix:")
print(str(m))
f1 = f1_score(Y, P2)
print("f1_score:")
print(str(f1))
accuracy = accuracy_score(Y, P2)
print("accuracy:")
print(str(accuracy))

print("M3:")
m = confusion_matrix(Y, P3)
print("Confusion matrix:")
print(str(m))
f1 = f1_score(Y, P3)
print("f1_score:")
print(str(f1))
accuracy = accuracy_score(Y, P3)
print("accuracy:")
print(str(accuracy))

print("M4:")
m = confusion_matrix(Y, P4)
print("Confusion matrix:")
print(str(m))
f1 = f1_score(Y, P4)
print("f1_score:")
print(str(f1))
accuracy = accuracy_score(Y, P4)
print("accuracy:")
print(str(accuracy))
