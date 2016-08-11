import os
import glob
from datetime import datetime, timedelta
from weather import downloadWeatherDataFromWunderground,\
    downloadWeatherForecastFromWunderground, processWUData, appendForecastData
from Timestamp import Timestamp
from yorktime import createTimeFile
from topobuildings import multiplyBuildingData
from osmpolygons import multiplyLanduseData
from traffic import addTimestampToTraffic
from join import joinFiles
from data.data import loadData
from models.model_randomforest import trainRandomForest, applyRandomForest
import sys
import matplotlib.pyplot as plt
from matplotlib import dates
from airquality import downloadYorkAirqualityData
from numpy import NAN
from eval.rmse import rmseEval
from eval.mae import maeEval
from eval.correlation import correlationEval
from rectangles import loadRectangles

DIRECTORY = "/media/sf_lur/forecast/"
 
if len(sys.argv) > 1:
    DIRECTORY = sys.argv[1]
     
DATA_DIRECTORY = DIRECTORY + "data/"
DATAPRE_DIRECTORY = DIRECTORY + "data_pre/"
OUTPUT_DIRECTORY = DIRECTORY + "output/"
WU_HISTORY_DIRECTORY = DIRECTORY + "data_wu_history/"
 
print("DATA_DIRECTORY: " + DATA_DIRECTORY)
print("DATAPRE_DIRECTORY: " + DATAPRE_DIRECTORY)
print("OUTPUT_DIRECTORY: " + OUTPUT_DIRECTORY)
print("WU_HISTORY_DIRECTORY: " + WU_HISTORY_DIRECTORY)
 
wuKey = "0ec4fab9d96c8700"
        
# generate timestamps
print("Generate timestamps...")
     
todayString = datetime.now().strftime('%Y%m%d')
currentYear = int(datetime.now().strftime('%Y'))
currentMonth = int(datetime.now().strftime('%m'))
currentDay = int(datetime.now().strftime('%d'))
currentHour = int(datetime.now().strftime('%H'))
     
tomorrow = (datetime.now() + timedelta(days=1))
tomorrowString = tomorrow.strftime('%Y%m%d')
tomorrowYear = int(tomorrow.strftime('%Y'))
tomorrowMonth = int(tomorrow.strftime('%m'))
tomorrowDay = int(tomorrow.strftime('%d'))
      
print("\tToday's day stamp: " + todayString)
print("\tTomorrow's day stamp: " + tomorrowString)
print("\tCurrent year, month, day, hour: " + str(currentYear) + "," + str(currentMonth) + "," + str(currentDay) + "," + str(currentHour))
print("\tTomorrow year, month, day: " + str(tomorrowYear) + "," + str(tomorrowMonth) + "," + str(tomorrowDay))
     
timestamps = []
historyTimestamps = []
forecastTimestamps = []
for hour in range(0, currentHour + 1):
    timestamp = Timestamp().createBasedOnOther(currentYear, currentMonth, currentDay, hour)
    historyTimestamps.append(timestamp)
     
for hour in range(0, 24):
    timestamp = Timestamp().createBasedOnOther(currentYear, currentMonth, currentDay, hour)
    timestamps.append(timestamp)
    if timestamp not in historyTimestamps:
        forecastTimestamps.append(timestamp) 
     
for hour in range(0, 24):
    timestamp = Timestamp().createBasedOnOther(tomorrowYear, tomorrowMonth, tomorrowDay, hour)
    timestamps.append(timestamp)
    forecastTimestamps.append(timestamp)
         
# print("History " + str(len(historyTimestamps)))
# for t in historyTimestamps:
#     print(str(t))
# print("Forecast " + str(len(forecastTimestamps))) 
# for t in forecastTimestamps:
#     print(str(t))
       
print("Done...")
 
# remove everything from the data folder
print("Remove all files from data directory " + DATA_DIRECTORY)
       
files = glob.glob(DATA_DIRECTORY + '*')
for f in files:
    os.remove(f)
       
print("Done...")
     
# remove everything from the output folder
print("Remove all files from output directory " + OUTPUT_DIRECTORY)
       
files = glob.glob(OUTPUT_DIRECTORY + '*')
for f in files:
    os.remove(f)
       
print("Done...")
       
print("Download today's weather history...")
# download today's weather history
          
downloadWeatherDataFromWunderground(
    wuKey, 
    "UK", 
    "York", 
    [todayString], 
    DATA_DIRECTORY + "", 
    8.0,
    "\t")
          
# rename the downloaded file
          
print("\tRenaming " + DATA_DIRECTORY + "york_" + todayString + ".json" + " to " + DATA_DIRECTORY + "wu_history.json")
          
os.rename(DATA_DIRECTORY + "york_" + todayString + ".json", DATA_DIRECTORY + "wu_history.json")
          
print("Done...")
          
print("Downloading today's + tomorrow's weather forecast...")
# download forecast for today/tomorrow
          
downloadWeatherForecastFromWunderground(
    wuKey, 
    "UK", 
    "York", 
    DATA_DIRECTORY + "wu_forecast.json", 
    8.0, 
    "\t")
          
print("Done...")
       
print("Process weather data...")
# generate weather data
        
processWUData(
    historyTimestamps,
    DATA_DIRECTORY, 
    DATAPRE_DIRECTORY + "grid_rectangles.csv",
    DATA_DIRECTORY + "weather.csv", 
    "\t",
    ["wu_history.json"])
       
appendForecastData(
    forecastTimestamps, 
    DATA_DIRECTORY + "wu_forecast.json", 
    DATAPRE_DIRECTORY + "grid_rectangles.csv", 
    DATA_DIRECTORY + "weather.csv", 
    "\t")
       
print("Done...")      
       
# generate time related data
print("Generating time related data...")
createTimeFile(
    timestamps, 
    DATAPRE_DIRECTORY + "grid_rectangles.csv",
    DATA_DIRECTORY + "yorktime.csv",
    "\t")
          
print("Done...")
       
# generate topo data
print("Generating topo data...")
multiplyBuildingData(
    DATAPRE_DIRECTORY + "topo_100_2015.csv", 
    timestamps, 
    DATA_DIRECTORY + "topo_timestamp.csv", 
    "\t")
print("Done...")
       
# generate landuse data
print("Generating osm landuse data...")
multiplyLanduseData(
    DATAPRE_DIRECTORY + "osmpoly_100_2015.csv", 
    timestamps, 
    DATA_DIRECTORY + "osmlanduse.csv", 
    "\t")
print("Done...")
       
# generate traffic data
print("Generating traffic data...")
addTimestampToTraffic(
    timestamps, 
    DATAPRE_DIRECTORY + "traffic.csv", 
    DATA_DIRECTORY + "traffic.csv", 
    "\t")
       
# join the data
print("Joining preprocessed files...")
filesToJoin = [
    DATA_DIRECTORY + "topo_timestamp.csv",
    DATA_DIRECTORY + "traffic.csv",
    DATA_DIRECTORY + "osmlanduse.csv",
    DATA_DIRECTORY + "weather.csv",
    DATA_DIRECTORY + "yorktime.csv"]
             
joinFiles(
    filesToJoin,
    DATA_DIRECTORY + "data.csv",
    True,
    "\t")
print("Done...")
     
# learn the model
trainDataFile = DATAPRE_DIRECTORY + "data_hour_2015.csv"
print("Load the data for training the model from " + trainDataFile + "...")
trainData = {}
trainColumns = []
loadData(trainDataFile, ["location", "timestamp"], trainData, trainColumns)
      
print("Done...")
      
print("Train the model...")
      
model = trainRandomForest(trainData, trainColumns, "target", {'estimators': 59, 'leaf': 9})
      
print("Done...")
     
# apply model on the joined data
     
applyDataFile = DATA_DIRECTORY + "data.csv"
     
print("Load data the prepared data from " + applyDataFile + "...")
applyData = {}
applyColumns = []
loadData(applyDataFile, [], applyData, applyColumns)
print("Done...")
     
print("Apply the model...")
     
predictionData = applyRandomForest(applyData, model, {'estimators': 59, 'leaf': 9})
     
print("Done...")
     
# generate output
     
print("Generate output...")
     
finalData = {}
for timestamp in timestamps:
    finalData[timestamp.key] = {}
     
for i in range(0, len(predictionData)):
    location = str(int(applyData["location"][i]))
    timestamp = str(int(applyData["timestamp"][i]))
    value = predictionData[i]
    finalData[timestamp][location] = value
# # json data output      
# for timestamp in timestamps:
#     fileName = OUTPUT_DIRECTORY + timestamp.key + ".json"
#     print("\tWriting data to " + fileName)
#     output = open(fileName, 'w')
#     output.write('{ "no2": [ \n')
#     firstRecord = True
#     for location in finalData[timestamp.key]:
#         if firstRecord:
#             firstRecord = False
#         else:
#             output.write("\n,")
#         output.write('{"id":' + location + ',"v":' + str(finalData[timestamp.key][location]) + "}")
#     output.write("\n]}\n")
#     output.close()
   
# # bytearray output
locationOrdered = []
for location in finalData[timestamps[0].key]:
    locationOrdered.append(int(location))
locationOrdered.sort()
for i in range(0, len(locationOrdered)):
    locationOrdered[i] = str(locationOrdered[i])
       
for timestamp in timestamps:
    fileName = OUTPUT_DIRECTORY + timestamp.key + ".dat"
    print("\tWriting data to " + fileName)
    output = open(fileName, 'wb')
    if timestamp.key in finalData:
        for location in locationOrdered:
            if location in finalData[timestamp.key]:
                level = finalData[timestamp.key][location]
                levelInt = int(level * 100.0)
                levelUpper = levelInt // 256
                levelDown = levelInt % 256
        #         output.write(levelUpper)
        #         output.write(levelDown)
                output.write(bytes([levelUpper, levelDown]))
    output.close()
     
print("Done...")

# generate day string for the last 2 weeks
 
print("Generate day string and timestamps for the last 2 weeks")
 
pastweeksTimestamps = []
pastweeksDays = []
for i in range(1, 15):
    d = (datetime.now() - timedelta(days=i))
    dayString = d.strftime('%Y%m%d')
    for h in range(0, 24):
        if (h < 10):
            timestampKey = dayString + "0" + str(h)
        else:
            timestampKey = dayString + str(h)
        timestamp = Timestamp().createBasedOnKey(timestampKey)
        pastweeksTimestamps.append(timestamp)
         
    pastweeksDays.append(dayString)
     
print("Done...")

print("Getting aq information for the last two weeks...")

aqData = downloadYorkAirqualityData(
    pastweeksTimestamps[len(pastweeksTimestamps) - 1],
    pastweeksTimestamps[0],
    DATAPRE_DIRECTORY + "stations_rectangles.csv",
    "\t"
    )

print("Done...")
 
print("Download wu data for the last 2 weeks...")
  
downloadWeatherDataFromWunderground(
    wuKey, 
    "UK", 
    "York", 
    pastweeksDays, 
    WU_HISTORY_DIRECTORY, 
    8.0,
    "\t")
  
print("Done...")
  
print("Process weather data...l")
# generate weather data
         
processWUData(
    pastweeksTimestamps,
    WU_HISTORY_DIRECTORY, 
    DATAPRE_DIRECTORY + "stations_rectangles.csv",
    DATA_DIRECTORY + "pw_weather.csv", 
    "\t")
        
print("Done...")      
        
# generate time related data
print("Generating time related data...")
createTimeFile(
    pastweeksTimestamps, 
    DATAPRE_DIRECTORY + "stations_rectangles.csv",
    DATA_DIRECTORY + "pw_time.csv",
    "\t")
           
print("Done...")
        
# generate topo data
print("Generating topo data...")
multiplyBuildingData(
    DATAPRE_DIRECTORY + "topo_2015.csv", 
    pastweeksTimestamps, 
    DATA_DIRECTORY + "pw_topo.csv", 
    "\t")
print("Done...")
        
# generate landuse data
print("Generating osm landuse data...")
multiplyLanduseData(
    DATAPRE_DIRECTORY + "osmpoly_2015.csv", 
    pastweeksTimestamps, 
    DATA_DIRECTORY + "pw_osmpoly.csv", 
    "\t")
print("Done...")
        
# generate traffic data
print("Generating traffic data...")
addTimestampToTraffic(
    pastweeksTimestamps, 
    DATAPRE_DIRECTORY + "stations_traffic.csv", 
    DATA_DIRECTORY + "pw_traffic.csv", 
    "\t")
        
# join the data
print("Joining preprocessed files...")
filesToJoin = [
    DATA_DIRECTORY + "pw_topo.csv",
    DATA_DIRECTORY + "pw_traffic.csv",
    DATA_DIRECTORY + "pw_osmpoly.csv",
    DATA_DIRECTORY + "pw_weather.csv",
    DATA_DIRECTORY + "pw_time.csv"]
              
joinFiles(
    filesToJoin,
    DATA_DIRECTORY + "pw_data.csv",
    True,
    "\t")
print("Done...")
      
      
# apply model on the joined data
      
applyDataFile = DATA_DIRECTORY + "pw_data.csv"
      
print("Load data the prepared data from " + applyDataFile + "...")
applyData = {}
applyColumns = []
loadData(applyDataFile, [], applyData, applyColumns)
print("Done...")
      
print("Apply the model...")
      
predictionData = applyRandomForest(applyData, model, {'estimators': 59, 'leaf': 9})
      
print("Done...")
 
# generate output
      
# load rectangles
rectangles = []
loadRectangles(rectangles, DATAPRE_DIRECTORY + "stations_rectangles.csv")
rectanglesMap = {}
for rectangle in rectangles:
    rectanglesMap[str(rectangle.ID)] = rectangle
 
print("Generate outputs...")
      
finalData = {}
for timestamp in pastweeksTimestamps:
    finalData[timestamp.key] = {}
 
locations = set()
      
for i in range(0, len(predictionData)):
    location = str(int(applyData["location"][i]))
    locations.add(location)
    timestamp = str(int(applyData["timestamp"][i]))
    value = predictionData[i]
    finalData[timestamp][location] = value
 
orderedTimestampKeys = []
for timestamp in pastweeksTimestamps:
    orderedTimestampKeys.append(timestamp.key)
orderedTimestampKeys.sort()
 
orderedTimestamps = []
for timestampKey in orderedTimestampKeys:
    orderedTimestamps.append(Timestamp().createBasedOnKey(timestampKey))
     
for loc in locations:
    station = rectanglesMap[str(loc)].name
    print(str(loc) + " -> " + station)
    modelledData = []
    aqDataStation = []
    datesList = []
    observed = []
    predicted = []
    for timestamp in orderedTimestamps:
        modelledData.append(finalData[timestamp.key][loc])
        d = datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour)
        datesList.append(d)
        if timestamp.key not in aqData or str(loc) not in aqData[timestamp.key]:
            aqDataStation.append(NAN)
        else:
            aqDataStation.append(aqData[timestamp.key][str(loc)])
            observed.append(aqData[timestamp.key][str(loc)])
            predicted.append(finalData[timestamp.key][loc])
    
    if len(predicted) > 0: 
        rmse = rmseEval(predicted, observed)
        mae = maeEval(predicted, observed)
        r = correlationEval(predicted, observed)
#     print("r: " + str(r))
#     print("RMSE: " + str(rmse))
#     print("MAE: " + str(mae))
         
    fig = plt.figure(None, figsize=(15, 9))
    ax = fig.add_subplot(111)
    hfmt = dates.DateFormatter('%d/%m/%Y %H:%M')
    ax.xaxis.set_major_formatter(hfmt)
    if len(predicted) > 0:
        ax.plot_date(datesList, modelledData, '-', color="b", label="Modelled (RMSE:" + str(rmse[1])[0:5] + ",MAE:" + str(mae[1])[0:5] + ",r:" + str(r[1])[0:4] + ")")
    else:
        ax.plot_date(datesList, modelledData, '-', color="b", label="Modelled")
    ax.plot_date(datesList, aqDataStation, '-', color="r", label="Observed")
    ax.legend()
    plt.ylabel("No2 concentration level (ug/m3)")
    plt.xlabel("Date")
    plt.title("No2 concentration levels at " + station)
    plt.savefig(OUTPUT_DIRECTORY + "history_" + station.lower() + ".png")    
          
print("Done...")

