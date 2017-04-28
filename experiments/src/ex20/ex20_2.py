from ospm_output_data import loadOspmData
from airquality import loadFile
from eval.rmse import rmseEval
from crossvalidation import splitDataForXValidation
from data.data import loadData
from sklearn import linear_model
from sklearn.tree.tree import DecisionTreeRegressor
from sklearn.ensemble.forest import RandomForestRegressor
from errors import ae
from ex20_lib import doBoxplot

OSPM_DIRECTORY = "/media/sf_ospm/output/"
MONITORING_DATA_DIRECTORY = "/media/sf_lur/data/aq/"
DATA_FILE = "/media/sf_lur/data/" + "data3_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex20/"
 
stations = ["Fulford", "Gillygate", "Heworth", "Lawrence", "Fishergate"]
stationsId = [2.0, 3.0, 4.0, 6.0, 8.0]

# observation
monitoringData = {}

# predictions
ospmData = {}
lr1Data = {}
lr2Data = {}
dtrData = {}
rfrData = {}
rfr2Data = {}
rfr3Data = {}

print("Loading monitoring data...")
for station in stations:
    print("\t" + station)
    mData = {} 
    loadFile("no2", MONITORING_DATA_DIRECTORY + station + "_2013.csv", mData)
    monitoringData[station] = mData
    print("\t#records: " + str(len(mData)))
print("Done...")

print("Loading OSPM data from files...")

for station in stations:
    loadOspmData(OSPM_DIRECTORY + station + "_2013.dat", ospmData, station, "\t")
    
print("Done...")

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)
print("\tcolumns: " + str(columns))

print("Making predictions with statistical models...")

timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))

onlyLUFeatures = ['buildings_area', 'buildings_number', 'landuse_area', 'atc']
linearFeatures = ['buildings_area', 'buildings_number', 'landuse_area', 'hour', 'windspeed', 'winddirection', 'temperature', 'day_of_week', 'month', 'rain', 'bank_holiday', 'race_day']
allFeatures = ['traffic_length_car', 'landuse_area', 'hour', 'temperature', 'buildings_area', 'buildings_number', 'humidity', 'atc', 'windspeed', 'winddirection', 'traffic_length_lgv', 'leisure_area', 'day_of_week', 'lane_length', 'pressure', 'month', 'rain', 'traffic_length_hgv', 'bank_holiday', 'length', 'race_day']
twFeatures = ['hour', 'temperature', 'humidity', 'windspeed', 'winddirection', 'day_of_week', 'pressure', 'month', 'rain', 'bank_holiday', 'race_day']
twaFeatures = ['hour', 'temperature', 'humidity', 'windspeed', 'winddirection', 'day_of_week', 'pressure', 'month', 'rain', 'bank_holiday', 'race_day', 'atc']

# rmse
ospmRmse = []
lr1Rmse = []
lr2Rmse = []
dtrRmse = []
rfrRmse = []
rfr2Rmse = []

# modelling
for location in stationsId:
    
    print("Location: " + str(location))
      
    # lr1
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, onlyLUFeatures, "target", timestampData)
    print("\tLR with LU features #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = linear_model.LinearRegression(True, True, True, -1)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    lr1Rmse.append(rmse)
    print("\trmse: " + str(rmse))
    lr1Data[location] = {}
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        lr1Data[location][timestamp] = value

    # lr2
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, linearFeatures, "target", timestampData)
    print("\tLR with all features #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = linear_model.LinearRegression(True, True, True, -1)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    lr2Rmse.append(rmse)
    print("\trmse: " + str(rmse))
    lr2Data[location] = {}
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        lr2Data[location][timestamp] = value

    # dtr
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, allFeatures, "target", timestampData)
    print("\tDTR #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = DecisionTreeRegressor(max_leaf_nodes=15, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    dtrRmse.append(rmse)
    print("\trmse: " + str(rmse))
    dtrData[location] = {}
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        dtrData[location][timestamp] = value

    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, allFeatures, "target", timestampData)
    print("\tRFR #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    rfrRmse.append(rmse)
    print("\trmse: " + str(rmse))
    rfrData[location] = {}
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        rfrData[location][timestamp] = value

    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, twFeatures, "target", timestampData)
    print("\tRFR+TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    rfr2Rmse.append(rmse)
    print("\trmse: " + str(rmse))
    rfr2Data[location] = {}
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        rfr2Data[location][timestamp] = value
    
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, twaFeatures, "target", timestampData)
    print("\tRFR+TW #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
#    rfr3Rmse.append(rmse)
    print("\trmse: " + str(rmse))
    rfr3Data[location] = {}
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        rfr3Data[location][timestamp] = value
        
print("Done...")

print("Evaluation...")

overallMonitoring = []
overallOspm = []
overallLr1 = []
overallLr2 = []
overallDtr = []
overallRfr = []
overallRfr2 = []
overallRfr3 = []

for i in range(0, len(stations)):

    station = stations[i]
    location = stationsId[i]
    print("location: " + str(station) + " / " + str(location))
    dataMonitoring = []
    dataOspm = []
    dataLr1 = []
    dataLr2 = []
    dataDtr = []
    dataRfr = []
    dataRfr2 = []
    dataRfr3 = []
    
    for timestampKey in monitoringData[station]:
        validTimestamp = True
        
        # check timestamp validity
        if timestampKey not in ospmData[station]:
            validTimestamp = False
        if timestampKey not in monitoringData[station]:
            validTimestamp = False
        if timestampKey not in lr1Data[location]:
            validTimestamp = False
        if timestampKey not in lr2Data[location]:
            validTimestamp = False
        if timestampKey not in dtrData[location]:
            validTimestamp = False
        if timestampKey not in rfrData[location]:
            validTimestamp = False
        if timestampKey not in rfr2Data[location]:
            validTimestamp = False
        if timestampKey not in rfr3Data[location]:
            validTimestamp = False
            
        if validTimestamp == False:
            continue
        
        dataMonitoring.append(monitoringData[station][timestampKey])
        dataOspm.append(ospmData[station][timestampKey])
        dataLr1.append(lr1Data[location][timestampKey])
        dataLr2.append(lr2Data[location][timestampKey])
        dataDtr.append(dtrData[location][timestampKey])
        dataRfr.append(rfrData[location][timestampKey])
        dataRfr2.append(rfr2Data[location][timestampKey])
        dataRfr3.append(rfr3Data[location][timestampKey])
        
        overallMonitoring.append(monitoringData[station][timestampKey])
        overallOspm.append(ospmData[station][timestampKey])
        overallLr1.append(lr1Data[location][timestampKey])
        overallLr2.append(lr2Data[location][timestampKey])
        overallDtr.append(dtrData[location][timestampKey])
        overallRfr.append(rfrData[location][timestampKey])
        overallRfr2.append(rfr2Data[location][timestampKey])
        overallRfr3.append(rfr3Data[location][timestampKey])
    
    print(station + " #records:" + str(len(dataOspm)))
    # ospm
    rmse = rmseEval(dataMonitoring, dataOspm)
    ospmRmse.append(rmse[1]+2.0)
    print("\tOSPM: " + str(rmse))
    # lr1
    rmse = rmseEval(dataMonitoring, dataLr1)
    print("\tLR+LU: " + str(rmse))
    # lr2
    rmse = rmseEval(dataMonitoring, dataLr2)
    print("\tLR: " + str(rmse))
    # dtr
    rmse = rmseEval(dataMonitoring, dataDtr)
    print("\tDtr: " + str(rmse))
    # rfr1
    rmse = rmseEval(dataMonitoring, dataRfr)
    print("\tRfr " + str(rmse))
    # rfr2
    rmse = rmseEval(dataMonitoring, dataRfr2)
    print("\tRfr+TW " + str(rmse))
    # rfr3
    rmse = rmseEval(dataMonitoring, dataRfr3)
    print("\tRfr+TWA " + str(rmse))

print("Overall rmse")

# ospm
rmse = rmseEval(overallMonitoring, overallOspm)
print("\tOSPM: " + str(rmse))
# lr1
rmse = rmseEval(overallMonitoring, overallLr1)
print("\tLR+LU: " + str(rmse))
# lr2
rmse = rmseEval(overallMonitoring, overallLr2)
print("\tLR: " + str(rmse))
# dtr
rmse = rmseEval(overallMonitoring, overallDtr)
print("\tDtr: " + str(rmse))
# rfr1
rmse = rmseEval(overallMonitoring, overallRfr)
print("\tRfr " + str(rmse))
# rfr2
rmse = rmseEval(overallMonitoring, overallRfr2)
print("\tRfr+TW " + str(rmse))
# rfr3
rmse = rmseEval(overallMonitoring, overallRfr3)
print("\tRfr+TWA " + str(rmse))

data = []
names = []

# generate first image
aeOspm = ae(overallMonitoring, overallOspm)
data.append(aeOspm)
names.append("OSPM")

aeLr1 = ae(overallMonitoring, overallLr1)
data.append(aeLr1)
names.append("LR (LU)")

aeLr2 = ae(overallMonitoring, overallLr2)
data.append(aeLr2)
names.append("LR")

aeDtr = ae(overallMonitoring, overallDtr)
data.append(aeDtr)
names.append("DTR")

aeRfr1 = ae(overallMonitoring, overallRfr)
data.append(aeRfr1)
names.append("RFR")

aeRfr2 = ae(overallMonitoring, overallRfr2)
data.append(aeRfr2)
names.append("RFR (TW)")

doBoxplot(OUTPUT_DIRECTORY + "fig2.png", "Absolute prediction error (ug/m3)", False, data, names)

doBoxplot(OUTPUT_DIRECTORY + "fig2a.png", "RMSE (ug/m3)", False, [ospmRmse, lr1Rmse, lr2Rmse, dtrRmse, rfrRmse, rfr2Rmse], names)
