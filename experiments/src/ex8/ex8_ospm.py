from sklearn import linear_model
from eval.rmse import rmseEval

def ospm(week, timestampWeekCategory, stationNames, ospmData2013, ospmData2014, data2013, data2014):
    trainTimestamps = set()
    ospmTrainData = {}
    for station in ospmData2013:
        ospmTrainData[station] = {}
        for timestamp in ospmData2013[station]:
            weekC = timestampWeekCategory[timestamp]
            if int(weekC) >= week:
                trainTimestamps.add(str(timestamp))
                ospmTrainData[station][timestamp] = ospmData2013[station][timestamp]
    
    observationTrainData = {}
    for station in ospmData2013:
        observationTrainData[station] = {}
    
    for i in range(0, len(data2013["target"])):
        timestamp = str(int(data2013["timestamp"][i]))
        location = stationNames[str(data2013["location"][i])]
        value = data2013["target"][i]
        observationTrainData[location][str(timestamp)] = value
    
    X = []
    y = []
    
    for station in ospmData2013:
        for timestamp in trainTimestamps:
            try:
                obs = observationTrainData[station][str(timestamp)]
                ospmPred = ospmTrainData[station][str(timestamp)]
                X.append([ospmPred])
                y.append(obs)
            except:
                a = 0
    
#     print(str(len(X)))
    
    model = linear_model.LinearRegression(True, True, True, -1)
    model.fit(X, y)
    
#     print(str(model.intercept_))
#     print(str(model.coef_))
    
    testTimestamps = set()
    ospmTestData = {}
    for station in ospmData2014:
        ospmTestData[station] = {}
        for timestamp in ospmData2014[station]:
            testTimestamps.add(str(timestamp))
            ospmTestData[station][timestamp] = ospmData2014[station][timestamp]
    
    observationTestData = {}
    for station in ospmData2014:
        observationTestData[station] = {}
    
    for i in range(0, len(data2014["target"])):
        timestamp = str(int(data2014["timestamp"][i]))
        location = stationNames[str(data2014["location"][i])]
        value = data2014["target"][i]
        observationTestData[location][str(timestamp)] = value
    
    X = []
    y = []
    
    for station in ospmData2014:
        for timestamp in testTimestamps:
            try:
                obs = observationTestData[station][str(timestamp)]
                ospmPred = ospmTestData[station][str(timestamp)]
                X.append([ospmPred])
                y.append(obs)
            except:
                a = 0
    
#     print(str(len(X)))
    
    prediction = model.predict(X)
    rmse = rmseEval(y, prediction)
    return rmse
    