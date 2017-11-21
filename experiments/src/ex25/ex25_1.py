from data.data import loadData
from ex25.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_FILE = "/experiments/ex25/file2.csv"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))

columnsGrouped = {
    "T": ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day'],
    "W": ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure'],
    "A": ['atc'],
    "R": ['lane_length', 'length'],
    "L": ['landuse_area', 'leisure_area'],
    "B": ['buildings_area', 'buildings_number']
    }

output = open(OUTPUT_FILE, 'w')
output.write("location,timestamp,tag,value\n")

def doEval(dataGroup):
    tag = ""
    for d in dataGroup:
        tag = tag + d
    features = []
    for dg in dataGroup:
        for d in columnsGrouped[dg]:
            features.append(d)
    print("Eval " + str(dataGroup) + " with features " + str(features))
    
    for location in locations:
        print("\tlocation: " + str(location))
        trainX, testX, trainY, testY, _, testTimestamp = splitDataForXValidation(location, "location", data, features, "target", timestampData)
        print("\t\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        rmse = rmseEval(testY, prediction)[1]
        print("\t\trmse: " + str(rmse))
        for i in range(0, len(prediction)):
            output.write(str(location) + ",")
            output.write(str(int(testTimestamp[i])) + ",")
            output.write(tag + ",")
            output.write(str(prediction[i]))
            output.write("\n")
        output.flush()

# for t in [True, False]:
#     for w in [True, False]:
#         for a in [True, False]:
#             for r in [True, False]:
#                 for l in [True, False]:
#                     for b in [True, False]:
#                         dataGroup = []
#                         if t: dataGroup.append("T")
#                         if w: dataGroup.append("W")
#                         if a: dataGroup.append("A")
#                         if r: dataGroup.append("R")
#                         if l: dataGroup.append("L")
#                         if b: dataGroup.append("B")
#                         if len(dataGroup) == 0:
#                             continue
#                         doEval(dataGroup) 

doEval(["T", "W"])
doEval(["T", "W", "L"])

output.close()
            