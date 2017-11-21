from data.data import loadData
from ex27.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_DIRECTORY = "/experiments/ex27/"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, ['timestamp'], data, columns)

sampleRate = 0.75

tw_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure'] 

allObs = []
allPrediction = []
 
for location in locations:
    print("Location: " + str(location))
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, tw_features, "target")
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
    model.fit(trainX, trainY)
    testPrediction = model.predict(testX)
    rmse = str(rmseEval(testY, testPrediction)[1])
    print("\tT+W rmse: " + rmse)
    for x in testY:
        allObs.append(x)
    for x in testPrediction:
        allPrediction.append(x)
    
print("Overall")    
rmse = str(rmseEval(allObs, allPrediction)[1])
print("\tRMSE: " + str(rmse))
