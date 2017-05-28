from data.data import loadData
from copy import deepcopy
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from sklearn.tree.tree import DecisionTreeClassifier
from crossvalidation import sample

DATA_FILE = "/media/sf_lur/data/" + "data3_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex19/"

locations = [2.0, 3.0, 4.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

# t+w
featuresTW = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day']
columnsTW = deepcopy(featuresTW)
columnsTW.extend(['location', 'timestamp', 'target'])

# t+w+a
featuresTWA = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'atc']
columnsTWA = deepcopy(featuresTWA)
columnsTWA.extend(['location', 'timestamp', 'target'])

columns2 = deepcopy(columns)
columns2.remove('location')
columns2.remove('target')
columns2.remove('timestamp')
    
# modelling
for location in locations:
    print("location: " + str(location))
    
    trainX, testX, trainY, testY, dataY = splitDataForXValidation(location, "location", data, featuresTW, columnsTW, "target")
    print("\tT+W #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    modelTW = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    modelTW.fit(trainX, trainY)
    predictionTrainTW = modelTW.predict(trainX)
    predictionTestTW = modelTW.predict(testX)
    
    trainX, testX, trainY, testY, dataY = splitDataForXValidation(location, "location", data, featuresTWA, columnsTWA, "target")
    print("\tT+W+A #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    modelTWA = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    modelTWA.fit(trainX, trainY)
    predictionTrainTWA = modelTWA.predict(trainX)
    predictionTestTWA = modelTWA.predict(testX)
    
    trainX, testX, trainY, testY, dataY = splitDataForXValidation(location, "location", data, columns2, columns, "target")
    label = []
    TWbetter = 0
    TWAbetter = 0
    for i in range(0, len(trainY)):
        aeTW = abs(predictionTrainTW[i] - trainY[i])
        aeTWA = abs(predictionTrainTWA[i] - trainY[i])
        if aeTW < aeTWA:
            TWbetter = TWbetter + 1
            label.append(0)
        else:
            TWAbetter = TWAbetter + 1
            label.append(1)
    
    print("\tTW better: " + str(TWbetter) + ", TWA better: " + str(TWAbetter))
    model = DecisionTreeClassifier(max_depth=9)
    model.fit(trainX, label)
    predictionTrainLabel = model.predict(trainX)
    predictionTestLabel = model.predict(testX)
    
    prediction = []
    for i in range(0, len(trainY)):
        if predictionTrainLabel[i] < 0.5:
            prediction.append(predictionTrainTW[i])
        else:
            prediction.append(predictionTrainTWA[i])
    
    prediction2 = []    
    for i in range(0, len(trainY)):
        aeTW = abs(predictionTrainTW[i] - trainY[i])
        aeTWA = abs(predictionTrainTWA[i] - trainY[i])
        if aeTW < aeTWA:
            prediction2.append(predictionTrainTW[i])
        else:
            prediction2.append(predictionTrainTWA[i])
    
    rmse = rmseEval(trainY, predictionTrainTW)[1]
    print("\tT+W train rmse: " + str(rmse))    
    rmse = rmseEval(trainY, predictionTrainTWA)[1]
    print("\tT+W+A train rmse: " + str(rmse))        
    rmse = rmseEval(trainY, prediction2)[1]
    print("\tbest combined train rmse: " + str(rmse))
    rmse = rmseEval(trainY, prediction)[1]
    print("\tcombined train rmse: " + str(rmse))
    
    prediction = []
    for i in range(0, len(testY)):
        if predictionTestLabel[i] < 0.5:
            prediction.append(predictionTestTW[i])
        else:
            prediction.append(predictionTestTWA[i])
            
    prediction2 = []    
    for i in range(0, len(testY)):
        aeTW = abs(predictionTestTW[i] - testY[i])
        aeTWA = abs(predictionTestTWA[i] - testY[i])
        if aeTW < aeTWA:
            prediction2.append(predictionTestTW[i])
        else:
            prediction2.append(predictionTestTWA[i])
    
    rmse = rmseEval(testY, predictionTestTW)[1]
    print("\tT+W rmse: " + str(rmse))    
    rmse = rmseEval(testY, predictionTestTWA)[1]
    print("\tT+W+A rmse: " + str(rmse))    
    rmse = rmseEval(testY, prediction2)[1]
    print("\tbest combined rmse: " + str(rmse))    
    rmse = rmseEval(testY, prediction)[1]
    print("\tcombined rmse: " + str(rmse))    

    trainX, testX, trainY, testY, dataY = splitDataForXValidation(location, "location", data, featuresTW, columnsTW, "target")
    trainX2, trainY2, testX2, testY2 = sample(0.8, trainX, trainY)
    print("\tT+W 0.8 #train: " + str(len(trainY2)) + ", #test:" + str(len(testY)))
    modelTW = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    modelTW.fit(trainX2, trainY2)
    predictionTestTW2 = modelTW.predict(testX2)
    predictionTestTW = modelTW.predict(testX)

    rmse = rmseEval(testY, predictionTestTW)[1]
    print("\tT+W 0.8 rmse: " + str(rmse))    

    trainX, testX, trainY, testY, dataY = splitDataForXValidation(location, "location", data, featuresTWA, columnsTWA, "target")
    trainX2, trainY2, testX2, testY2 = sample(0.8, trainX, trainY)
    print("\tT+W+A 0.8 #train: " + str(len(trainY2)) + ", #test:" + str(len(testY)))
    modelTWA = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    modelTWA.fit(trainX2, trainY2)
    predictionTestTWA2 = modelTWA.predict(testX2)
    predictionTestTWA = modelTWA.predict(testX)

    rmse = rmseEval(testY, predictionTestTWA)[1]
    print("\tT+W+A 0.8 rmse: " + str(rmse))    
    
    trainX, testX, trainY, testY, dataY = splitDataForXValidation(location, "location", data, columns2, columns, "target")
    trainX2, trainY2, testX2, testY2 = sample(0.8, trainX, trainY)
    label = []
    TWbetter = 0
    TWAbetter = 0
    for i in range(0, len(testY2)):
        aeTW = abs(predictionTestTW2[i] - testY2[i])
        aeTWA = abs(predictionTestTWA2[i] - testY2[i])
        if aeTW < aeTWA:
            TWbetter = TWbetter + 1
            label.append(0)
        else:
            TWAbetter = TWAbetter + 1
            label.append(1)
    
    print("\tTW better: " + str(TWbetter) + ", TWA better: " + str(TWAbetter))
    model = DecisionTreeClassifier(max_depth=9)
    model.fit(testX2, label)
    predictionTestLabel = model.predict(testX)
    
    prediction = []
    for i in range(0, len(testY)):
        if predictionTrainLabel[i] < 0.5:
            prediction.append(predictionTestTW[i])
        else:
            prediction.append(predictionTestTWA[i])
    
    rmse = rmseEval(testY, prediction)[1]
    print("\tT+W+A combined2 rmse: " + str(rmse))    
            