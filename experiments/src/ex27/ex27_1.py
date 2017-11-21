from data.data import loadData
from ex27.crossvalidation import splitDataForXValidation,\
    splitDataForXValidationSampled
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_DIRECTORY = "/experiments/ex27/"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

data = {}
columns = ['timestamp', 'location']
loadData(DATA_FILE, [], data, columns)

columnsTW = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure']

for location in locations:
    print("location: " + str(location))
    # save down trainX, trainY, testX, testY
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, columns, "target")
    print("\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
    model.fit(trainX, trainY)
    testPrediction = model.predict(testX)
    testRmse = str(rmseEval(testY, testPrediction)[1])
    print("\tRFR+All rmse: " + str(testRmse))
    
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, columnsTW, "target")
    print("\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
    model.fit(trainX, trainY)
    testPrediction = model.predict(testX)
    testRmse = str(rmseEval(testY, testPrediction)[1])
    print("\tRFR+TW rmse: " + str(testRmse))
    
    for sr in [0.95, 0.9, 0.85, 0.8, 0.75, 0.7]:
        print("sampleRate: " + str(sr))
        trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled(location, "location", sr, 42, data, columnsTW, "target")
        print("\t#train: " + str(len(trainY1)) + ", #test:" + str(len(testY)))
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
        model.fit(trainX1, trainY1)
        testPrediction = model.predict(testX)
        testRmse = str(rmseEval(testY, testPrediction)[1])
        print("\tRFR+TW rmse: " + str(testRmse))
        
