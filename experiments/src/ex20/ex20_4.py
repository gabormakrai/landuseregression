from data.data import loadData
from copy import deepcopy
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from ex20_lib import generateHeatmap, generateColorHeatmap
import math
from ex20_lib import doLineChart
from ex20_lib import writeOutWeeklyData

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
DATA_FILE2 = "/media/sf_lur/data/" + "data3_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex20/"

# wData = []
# d = []
# for i in range(0,168):
#     d.append(i)
# wData.append(d)
# wData.append(d)
# wData.append(d)
# d = []
# for i in range(0,168):
#     d.append(200-i)
# wData.append(d)
# wData.append(d)
# names = ["obs", "pred\n(TW)", "pred(TWA)", "error(TW)", "error(TWA)"]
# generateHeatmap(OUTPUT_DIRECTORY + "hello_13.png", wData, "No2 heatmap - week", names)
# exit()

locations = [2.0, 8.0]

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["8.0"] = "Fishergate"

print("Load data to generate observationData...")

# load data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)
 
observationData = {}
TWpredictionData = {}
TWAtcpredictionData = {}

for loc in locations:
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

timestampDoubleData2 = data2["timestamp"]
timestampData2 = []
for v in timestampDoubleData2:
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

week13Timestamps = []
week29Timestamps = []

week = 0
weekoftheday = 1
weeklyTimestamps = []
     
for month in range(1, 13):
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
         
        weekoftheday = weekoftheday + 1
         
        if weekoftheday == 8 and week == 13:
            week13Timestamps = deepcopy(weeklyTimestamps)
        if weekoftheday == 8 and week == 29:
            week29Timestamps = deepcopy(weeklyTimestamps)
            
                             
        if weekoftheday == 8:
            weekoftheday = 1
            week = week + 1
            weeklyTimestamps = []
             
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

def doSomething(station, timestamps, week, fName):

    names = []
    names.append(stationNames[str(location)])
    names.append("T+W")
    names.append("T+W+Atc")
    names.append("error (T+W)")
    names.append("error (T+W+Atc)")
    
    weeklyObservationData = []
    weeklyTWPredictionData = []
    weeklyTWAtcPredictionData = []
    for timestamp in timestamps:
        if str(timestamp) in observationData[str(station)]:
            weeklyObservationData.append(observationData[str(station)][str(timestamp)])
            weeklyTWPredictionData.append(TWpredictionData[str(station)][str(timestamp)])
            weeklyTWAtcPredictionData.append(TWAtcpredictionData[str(station)][str(timestamp)])
        else:
            weeklyObservationData.append(float('nan'))
            weeklyTWPredictionData.append(float('nan'))
            weeklyTWAtcPredictionData.append(float('nan'))
    
    wData = []
    
    # generate errors
    obs = weeklyObservationData
    predTW = weeklyTWPredictionData
    predTWA = weeklyTWAtcPredictionData
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
    
    wData.append(obs)
    wData.append(predTW)
    wData.append(predTWA)
    wData.append(errorTW)
    wData.append(errorTWA)
     
#    doLineChart(OUTPUT_DIRECTORY + stationNames[str(location)].lower() + "_" + str(week) + "l.png", "No2 prediction - week " + str(week) + " @ " + stationNames[str(location)], "Hour of the week", "No2 level (ug/m3)", wData, names)
     
    for i in range(0, len(errorTW)):
        if math.isnan(errorTW[i]) == False:
            errorTW[i] = errorTW[i] * 5.0
        if math.isnan(errorTWA[i]) == False:
            errorTWA[i] = errorTWA[i] * 5.0
     
#     for loc in locations:
#         if str(loc) != str(location):
#             wData.append(weeklyObservationData[str(loc)])
#             
#     wData.append(weeklyObservationData["5.0"])
#     wData.append(weeklyObservationData["7.0"])
#     for loc in locations:
#         if str(loc) != str(location):
#             names.append(stationNames[str(loc)])
#     names.append(stationNames["5.0"])
#     names.append(stationNames["7.0"])

    generateHeatmap(fName, wData, "No2 heatmap - week " + str(week), names)
     
#     names = []
#     names.append(stationNames[str(location)])
#     names.append("e(T+W)-e(T+W+A)")
#     wData = []
#     wData.append(weeklyObservationData[str(location)])
#     errorerror = []
#      
#     for i in range(0, len(errorTW)):
#         if math.isnan(errorTW[i]) or math.isnan(errorTWA[i]):
#             errorerror.append(float('nan'))
#         else:
#             errorerror.append(errorTW[i] - errorTWA[i])
#              
#     wData.append(errorerror)
#     doLineChart(OUTPUT_DIRECTORY + "error_" + stationNames[str(location)].lower() + "_" + str(week) + ".png", "No2 prediction errors - week " + str(week) + " @ " + stationNames[str(location)], "Hour of the week", "No2 level (ug/m3)", wData, names)
#      
#     names = []
#     names.append("errorTW")
#     names.append("errorTWA")
#     names.append("errordiff")
#     wData = []
#     wData.append(errorTW)
#     wData.append(errorTWA)
#     wData.append(errorerror)
#     writeOutWeeklyData(OUTPUT_DIRECTORY + "error_" + stationNames[str(location)].lower() + "_" + str(week) + ".csv", weeklyTimestamps, names, wData)


             

print("Week 13")
print(str(week13Timestamps[0]))
print(str(week13Timestamps[len(week13Timestamps)-1]))

print("Week 29")
print(str(week29Timestamps[0]))
print(str(week29Timestamps[len(week29Timestamps)-1]))

print("fulford 2.0 week 29")
doSomething(2.0, week29Timestamps, 29, OUTPUT_DIRECTORY + "fig5.png")

print("fishergate 8.0 week 13")
doSomething(8.0, week13Timestamps, 13, OUTPUT_DIRECTORY + "fig6.png")

