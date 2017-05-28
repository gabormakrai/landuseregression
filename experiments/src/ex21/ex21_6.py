from data.data import loadData
from collections import defaultdict
from ex21.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

DATA_FILE = "/data/london_hour_2015.csv"

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

loc61Data = defaultdict(list)
loc66Data = defaultdict(list)
loc51Data = defaultdict(list)

for i in range(0, len(data["location"])):
    if data["location"][i] == 61.0:
        for c in columns:
            loc61Data[c].append(data[c][i])
    if data["location"][i] == 66.0:
        for c in columns:
            loc66Data[c].append(data[c][i])
    if data["location"][i] == 51.0:
        for c in columns:
            loc51Data[c].append(data[c][i])

trainX, testX, trainY, testY = splitDataForXValidation(set([61.0]), set(), "location", loc61Data, columns, "target")
trainX2, testX2, trainY2, testY2 = splitDataForXValidation(set(), set([61.0]), "location", loc61Data, columns, "target")
model = RandomForestRegressor(max_depth=10, n_estimators = 60, n_jobs = -1, random_state=42)
model.fit(trainX, trainY)
prediction = model.predict(testX2)
rmse = rmseEval(testY2, prediction)[1]
print("Training on station 61, applying on station 61: rmse: " + str(rmse))

trainX, testX, trainY, testY = splitDataForXValidation(set([61.0]), set(), "location", loc61Data, columns, "target")
trainX2, testX2, trainY2, testY2 = splitDataForXValidation(set(), set([66.0]), "location", loc66Data, columns, "target")
model = RandomForestRegressor(max_depth=10, n_estimators = 60, n_jobs = -1, random_state=42)
model.fit(trainX, trainY)
prediction = model.predict(testX2)
rmse = rmseEval(testY2, prediction)[1]
print("Training on station 61, applying on station 66: rmse: " + str(rmse))

trainX, testX, trainY, testY = splitDataForXValidation(set([61.0]), set(), "location", loc61Data, columns, "target")
trainX2, testX2, trainY2, testY2 = splitDataForXValidation(set(), set([51.0]), "location", loc51Data, columns, "target")
model = RandomForestRegressor(max_depth=10, n_estimators = 60, n_jobs = -1, random_state=42)
model.fit(trainX, trainY)
prediction = model.predict(testX2)
rmse = rmseEval(testY2, prediction)[1]
print("Training on station 61, applying on station 51: rmse: " + str(rmse))
