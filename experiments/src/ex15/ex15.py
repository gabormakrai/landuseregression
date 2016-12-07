from data.data import loadData
from copy import deepcopy
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from ex15_lib import generateTimestampsForADay
from ex15_lib import doLineChart
from ex15_lib import doBoxplot

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
DATA_FILE2 = "/media/sf_lur/data/" + "data3_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex15/"

daysInInterest = []

daysInInterest.append( ("Fishergate", "20130114") )
daysInInterest.append( ("Fishergate", "20130410") )
daysInInterest.append( ("Fishergate", "20130528") )
daysInInterest.append( ("Fishergate", "20131115") )
daysInInterest.append( ("Fishergate", "20131125") )
daysInInterest.append( ("Fishergate", "20131126") )

daysInInterest.append( ("Fulford", "20130321") )
daysInInterest.append( ("Fulford", "20130723") )
daysInInterest.append( ("Fulford", "20130727") )

daysInInterest.append( ("Gillygate", "20131114") )
daysInInterest.append( ("Gillygate", "20131115") )
daysInInterest.append( ("Gillygate", "20131119") )
daysInInterest.append( ("Gillygate", "20131123") )
daysInInterest.append( ("Gillygate", "20131127") )

daysInInterest.append( ("Heworth", "20131011") )
daysInInterest.append( ("Heworth", "20131012") )

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

locations = [2.0, 3.0, 4.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)
 
observationData = {}
TWpredictionData = {}
TWAtcpredictionData = {}
WAtcpredictionData = {}

for loc in locations:
    observationData[str(loc)] = {}
    TWpredictionData[str(loc)] = {}
    TWAtcpredictionData[str(loc)] = {}
    WAtcpredictionData[str(loc)] = {}
    
for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    timestamp = str(int(data["timestamp"][i]))
    value = data["target"][i]
    if location in observationData:    
        observationData[location][timestamp] = value
        
data2 = {}
columns2 = []
loadData(DATA_FILE2, [], data2, columns2)

featureTW = []

# weather related
featureTW.append('winddirection')
featureTW.append('windspeed')
featureTW.append('temperature')
featureTW.append('rain')
featureTW.append('pressure')

# time related
featureTW.append('hour')
featureTW.append('day_of_week')
featureTW.append('month')
featureTW.append('bank_holiday')
featureTW.append('race_day')

#atc feature
featureTWAtc = deepcopy(featureTW)
featureTWAtc.append("atc")

featureWAtc = []
featureWAtc.append('winddirection')
featureWAtc.append('windspeed')
featureWAtc.append('temperature')
featureWAtc.append('rain')
featureWAtc.append('pressure')
featureWAtc.append("atc")


timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))

timestampDoubleData = data2["timestamp"]
timestampData2 = []
for v in timestampDoubleData:
    timestampData2.append(str(int(v)))

# modelling
for location in locations:
    
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, featureTW, "target", timestampData)
    print("\tT+W (on data without ATC) #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        TWpredictionData[str(location)][timestamp] = value
    
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data2, featureTWAtc, "target", timestampData2)                  
    print("\tT+W+Atc #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        TWAtcpredictionData[str(location)][timestamp] = value
        
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data2, featureWAtc, "target", timestampData2)                  
    print("\tW+Atc #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        value = prediction[i]
        WAtcpredictionData[str(location)][timestamp] = value
        
minValues = {}
maxValues = {}
for c in featureTWAtc:
    minV = float("+inf")
    maxV = float("-inf")
    for v in data2[c]:
        if minV > v:
            minV = v
        if maxV < v:
            maxV = v
    minValues[c] = minV
    maxValues[c] = maxV
    print(str(c) + " -> min: " + str(minV) + ", max: " + str(maxV))

minValues["windspeed"] = 0.0
        
for (station, day) in daysInInterest:
    stationId = 0.0
    for sId in stationNames:
        if stationNames[sId] == station:
            stationId = sId
            break
    timestamps = generateTimestampsForADay(day)
    
    dayObs = []
    dayTW = []
    dayTWA = []
    dayWA = []
    for timestamp in timestamps:
        dayObs.append(observationData[str(stationId)][timestamp])
        dayTW.append(TWpredictionData[str(stationId)][timestamp])
        dayTWA.append(TWAtcpredictionData[str(stationId)][timestamp])
        dayWA.append(WAtcpredictionData[str(stationId)][timestamp])
    
    names = []
    dData = []
        
    names.append("T+W")
    dData.append(dayTW)
    
    names.append("T+W+A")
    dData.append(dayTWA)
    
    names.append("W+A")
    dData.append(dayWA)
    
    names.append("Observation")
    dData.append(dayObs)
    
    names2 = []
    dData2 = []
    
    names2.append("error(T+W)")
    d = []
    for i in range(0, len(dayObs)):
        d.append(abs(dayTW[i] - dayObs[i]))
    dData2.append(d)
    
    names2.append("error(T+W+A)")
    d = []
    for i in range(0, len(dayObs)):
        d.append(abs(dayTWA[i] - dayObs[i]))
    dData2.append(d)
    
    names2.append("error(W+A)")
    d = []
    for i in range(0, len(dayObs)):
        d.append(abs(dayWA[i] - dayObs[i]))
    dData2.append(d)
    
#     names2.append("diff")
#     d = []
#     for i in range(0, len(dayObs)):
#         d.append(dData2[0][i] - dData2[1][i])
#     dData2.append(d)
    
    names3 = []
    dData3 = []
    for c in featureTWAtc:
        minV = minValues[c]
        maxV = maxValues[c]
        names3.append(c)
        d = []
        foundRecord = False
        for timestamp in timestamps:
            for i in range(0, len(data2["timestamp"])):
                if str(float(timestamp)) == str(data2["timestamp"][i]) and str(data2["location"][i]) == str(stationId):
                    value = data2[c][i]
                    value = (value - minV) / (maxV - minV)
                    d.append(value)
                    foundRecord = True
                    break
            if foundRecord == False:
                d.append(float("nan"))
        dData3.append(d)
    
    doLineChart(OUTPUT_DIRECTORY + station.lower() + "_" + day + ".png", "No2 prediction @ " + station + " @ " + day, dData, names, dData2, names2, dData3, names3)
         
    names2.append("e(T+W)-e(T+W+A)")
    d = []
    for i in range(0, 24):
        v = dData2[0][i] - dData2[1][i]
        d.append(v)
    dData2.append(d)
    
    names2.append("e(T+W)-e(W+A)")
    d = []
    for i in range(0, 24):
        v = dData2[0][i] - dData2[2][i]
        d.append(v)
    dData2.append(d)
    
    doBoxplot(OUTPUT_DIRECTORY + station.lower() + "_" + day + "b.png", "No2 prediction errors @ " + station + " / " + day, "conc. level (ug/m3)", dData2, names2)
