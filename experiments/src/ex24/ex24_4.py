from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor
from ex24.crossvalidation import splitDataForXValidation
from eval.rmse import rmseEval
import matplotlib.pyplot as plt

DATA_FILE = "/data/london3_hour_2016.csv"
OUTPUT_FILE = "/experiments/ex24/ex24_4.png"

all_stations = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

print(str(columns))

features_TW = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week']
features_TWA = ['rain', 'temperature', 'windspeed', 'winddirection', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'atc']
features_ALL = ['leisure_area', 'rain', 'temperature', 'atc', 'windspeed', 'lane_length', 'building_area', 'winddirection', 'landuse_area', 'humidity', 'pressure', 'bank_holiday', 'hour', 'month', 'day_of_week', 'building_count', 'length', 'natural_area']

dataDict = {}
rmseDict = {}

for location in all_stations:
    
    print("stations " + str(location))

    trainStations = set(float(station) for station in all_stations if station != location)
    testStations = set([float(location)])
    
    trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TW, "target")
    print("\tTW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    dataDict[str(location) + "_obs"] = testY
    ae = []
    for i in range(0, len(testY)):
        ae.append(abs(testY[i] - prediction[i]))
    dataDict[str(location) + "_ae_tw"] = ae
    rmseDict[str(location) + "_ae_tw"] = rmse
     
    trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_TWA, "target")
    print("\tTWA #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    ae = []
    for i in range(0, len(testY)):
        ae.append(abs(testY[i] - prediction[i]))
    dataDict[str(location) + "_ae_twa"] = ae
    rmseDict[str(location) + "_ae_twa"] = rmse

    trainX, testX, trainY, testY = splitDataForXValidation(trainStations, testStations, "location", data, features_ALL, "target")
    print("\tALL #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    ae = []
    for i in range(0, len(testY)):
        ae.append(abs(testY[i] - prediction[i]))
    dataDict[str(location) + "_ae_all"] = ae
    rmseDict[str(location) + "_ae_all"] = rmse

dataToPlot = []
names = []
for location in all_stations:
    names.append("Monitoring " + str(int(float(location))))
    dataToPlot.append(dataDict[str(location) + "_obs"])
    names.append("RFR+TW " + str(int(float(location))) + "\nRMSE:" + str(rmseDict[str(location) + "_ae_tw"])[0:5])
    dataToPlot.append(dataDict[str(location) + "_ae_tw"])
    names.append("RFR+TWA " + str(int(float(location))) + "\nRMSE:" + str(rmseDict[str(location) + "_ae_twa"])[0:5])
    dataToPlot.append(dataDict[str(location) + "_ae_twa"])
    names.append("RFR+ALL " + str(int(float(location))) + "\nRMSE:" + str(rmseDict[str(location) + "_ae_all"])[0:5])
    dataToPlot.append(dataDict[str(location) + "_ae_all"])

fig = plt.figure(figsize=(24 * 4, 10))
ax = fig.add_subplot(111)

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')

plt.title("Monitoring data and predictions")

plt.ylabel("(ug/m3)")
plt.ylim(-5.0, 300.0)

plt.savefig(OUTPUT_FILE)
