from data.data import loadData
from copy import deepcopy
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from ex14_lib import generateHeatmap, generateColorHeatmap
import math
from ex14_lib import doLineChart
from ex14_lib import writeOutWeeklyData

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
DATA_FILE2 = "/media/sf_lur/data/" + "data3_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex14/"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]
locations2 = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

# sNames = []
# for loc in locations:
#     sNames.append(stationNames[str(loc)])

print("Load data to generate observationData...")

# load data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)
 
observationData = {}
TWpredictionData = {}
TWAtcpredictionData = {}

for loc in locations2:
    observationData[str(loc)] = {}
    TWpredictionData[str(loc)] = {}
    TWAtcpredictionData[str(loc)] = {}
 
print("Generate observationData...")

for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    timestamp = str(int(data["timestamp"][i]))
    value = data["target"][i]
    if location in observationData:    
        observationData[location][timestamp] = value

print("Load data for T+W/T+W+Atc prediction...")

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
    
DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
 
week = 0
weekoftheday = 1
weeklyTimestamps = []
weeklyObservationData = {}
weeklyTWPredictionData = {}
weeklyTWAtcPredictionData = {}
     
for month in range(1, 13):
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
         
        weekoftheday = weekoftheday + 1
         
        if weekoftheday == 8 and week > 0:
            
            for location in locations:
                
                names = []
                names.append(stationNames[str(location)])
                names.append("T+W")
                names.append("T+W+Atc")
                names.append("error (T+W)")
                names.append("error (T+W+Atc)")
                
                wData = []
                wData.append(weeklyObservationData[str(location)])
                wData.append(weeklyTWPredictionData[str(location)])
                wData.append(weeklyTWAtcPredictionData[str(location)])
                # generate errors
                obs = weeklyObservationData[str(location)]
                predTW = weeklyTWPredictionData[str(location)]
                predTWA = weeklyTWAtcPredictionData[str(location)]
                errorTW = []
                errorTWA = []
                for i in range(0, len(obs)):
                    if math.isnan(obs[i]) or math.isnan(predTW[i]):
                        errorTW.append(float('nan'))
                    else:
                        errorTW.append(abs(predTW[i] - obs[i]))
                    if math.isnan(obs[i]) or math.isnan(predTWA[i]):
                        errorTWA.append(float('nan'))
                    else:
                        errorTWA.append(abs(predTWA[i] - obs[i]))
                wData.append(errorTW)
                wData.append(errorTWA)
                
                doLineChart(OUTPUT_DIRECTORY + stationNames[str(location)].lower() + "_" + str(week) + "l.png", "No2 prediction - week " + str(week) + " @ " + stationNames[str(location)], "Hour of the week", "No2 level (ug/m3)", wData, names)
                
                for i in range(0, len(errorTW)):
                    if math.isnan(errorTW[i]) == False:
                        errorTW[i] = errorTW[i] * 5.0
                    if math.isnan(errorTWA[i]) == False:
                        errorTWA[i] = errorTWA[i] * 5.0
                
                for loc in locations:
                    if str(loc) != str(location):
                        wData.append(weeklyObservationData[str(loc)])
                wData.append(weeklyObservationData["5.0"])
                wData.append(weeklyObservationData["7.0"])
                for loc in locations:
                    if str(loc) != str(location):
                        names.append(stationNames[str(loc)])
                names.append(stationNames["5.0"])
                names.append(stationNames["7.0"])
                generateHeatmap(OUTPUT_DIRECTORY + stationNames[str(location)].lower() + "_" + str(week) + ".png", wData, "No2 heatmap - week " + str(week), names)
                generateColorHeatmap(OUTPUT_DIRECTORY + stationNames[str(location)].lower() + "_" + str(week) + "c.png", wData, "No2 heatmap - week " + str(week), names)
                
                names = []
                names.append(stationNames[str(location)])
                names.append("e(T+W)-e(T+W+A)")
                wData = []
                wData.append(weeklyObservationData[str(location)])
                errorerror = []
                
                for i in range(0, len(errorTW)):
                    if math.isnan(errorTW[i]) or math.isnan(errorTWA[i]):
                        errorerror.append(float('nan'))
                    else:
                        errorerror.append(errorTW[i] - errorTWA[i])
                        
                wData.append(errorerror)
                doLineChart(OUTPUT_DIRECTORY + "error_" + stationNames[str(location)].lower() + "_" + str(week) + ".png", "No2 prediction errors - week " + str(week) + " @ " + stationNames[str(location)], "Hour of the week", "No2 level (ug/m3)", wData, names)
                
                names = []
                names.append("errorTW")
                names.append("errorTWA")
                names.append("errordiff")
                wData = []
                wData.append(errorTW)
                wData.append(errorTWA)
                wData.append(errorerror)
                writeOutWeeklyData(OUTPUT_DIRECTORY + "error_" + stationNames[str(location)].lower() + "_" + str(week) + ".csv", weeklyTimestamps, names, wData)
                             
        if weekoftheday == 8:
            weekoftheday = 1
            week = week + 1
            weeklyTimestamps = []
            for loc in locations2:
                weeklyObservationData[str(loc)] = []
                weeklyTWPredictionData[str(loc)] = []
                weeklyTWAtcPredictionData[str(loc)] = []               
             
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
            weeklyTimestamps.append(timestamp)
             
            for loc in locations2:
                if timestamp in observationData[str(loc)]:
                    weeklyObservationData[str(loc)].append(observationData[str(loc)][timestamp])
                else:
                    weeklyObservationData[str(loc)].append(float("nan"))
             
            for loc in locations:       
                if timestamp in TWpredictionData[str(loc)]:
                    weeklyTWPredictionData[str(loc)].append(TWpredictionData[str(loc)][timestamp])
                else:
                    weeklyTWPredictionData[str(loc)].append(float("nan"))
                    
                if timestamp in TWAtcpredictionData[str(loc)]:
                    weeklyTWAtcPredictionData[str(loc)].append(TWAtcpredictionData[str(loc)][timestamp])
                else:
                    weeklyTWAtcPredictionData[str(loc)].append(float("nan"))                    
                                 
#         