from data.data import loadData
from crossvalidation import findOutKForValidation
from graph import doLineChart
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex7/"

# load data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)
locationValues = findOutKForValidation("location", data)
timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))
 
observationData = {}
for loc in locationValues:
    observationData[str(loc)] = {}
 
for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    timestamp = str(int(data["timestamp"][i]))
    value = data["target"][i]    
    observationData[location][timestamp] = value
    
data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

columns.remove("location")

predictionData = {}
for location in locationValues:
    predictionData[str(location)] = {}

# modelling
for location in [6.0, 7.0]:
    
    trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data, columns, "target", timestampData)
    
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = 1, random_state=42)
    
    model.fit(trainX, trainY)
    
    prediction = model.predict(testX)
    
    rmse = rmseEval(testY, prediction)
    print(str(rmse))
    
    for i in range(0, len(testY)):
        timestamp = testTimestamp[i]
        predictionData[str(location)][timestamp] = prediction[i]
    
DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

week = 0
weekoftheday = 1

weeklyObservationData = {}
weeklyPredictionData = {}
    
for month in range(1, 13):
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
        
        weekoftheday = weekoftheday + 1
        
        if weekoftheday == 8 and week > 0:
            
            doLineChart(OUTPUT_DIRECTORY + "week_" + str(week) + ".png", "Week " + str(week) + " @ Lawrence&Nunnery" , "Hours of the week", "cLevel (ug/m3)", weeklyObservationData, weeklyPredictionData)
            
        if weekoftheday == 8:
            weekoftheday = 1
            week = week + 1
            for loc in locationValues:
                weeklyObservationData[str(loc)] = []
                weeklyPredictionData[str(loc)] = []
            
        if week < 1 or week > 51:
            continue
        
        if day < 10:
            dayString = "0" + str(day)
        else:
            dayString = str(day) 

        if month < 10:
            monthString = "0" + str(month)
        else:
            monthString = str(month)
        
        for hour in range(0, 24):
            if hour < 10:
                hourString = "0" + str(hour)
            else:
                hourString = str(hour)
        
            timestamp = "2013" + monthString + dayString + hourString
            
            if timestamp in observationData["6.0"]:
                weeklyObservationData["6.0"].append(observationData["6.0"][timestamp])
            else:
                weeklyObservationData["6.0"].append(float("nan"))
            
            if timestamp in observationData["7.0"]:
                weeklyObservationData["7.0"].append(observationData["7.0"][timestamp])
            else:
                weeklyObservationData["7.0"].append(float("nan"))
            
            if timestamp in predictionData["6.0"]:
                weeklyPredictionData["6.0"].append(predictionData["6.0"][timestamp])
            else:
                weeklyPredictionData["6.0"].append(float('nan'))
        
            if timestamp in predictionData["7.0"]:
                weeklyPredictionData["7.0"].append(predictionData["7.0"][timestamp])
            else:
                weeklyPredictionData["7.0"].append(float('nan'))
        
        