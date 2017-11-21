from data.data import loadData
import math
from ex28.ex28_lib import generateHeatmap, generateColorHeatmap
from collections import defaultdict

OUTPUT_DIRECTORY = "/experiments/ex28/ex28_2_"
DATA_FILE = "/experiments/ex28/ex28_1_data.csv"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

# load data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

observationData = defaultdict(lambda: defaultdict(lambda: []))
TWpredictionData = defaultdict(lambda: defaultdict(lambda: []))
TWApredictionData = defaultdict(lambda: defaultdict(lambda: []))
CombinedpredictionData = defaultdict(lambda: defaultdict(lambda: []))
CombinedTWorTWAData = defaultdict(lambda: defaultdict(lambda: []))

for i in range(0, len(data["timestamp"])):
    location = str(data["location"][i])
    timestamp = str(int(data["timestamp"][i]))
    obs = data["obs"][i]
    predTW = data["pred_TW"][i]
    predTWA = data["pred_TWA"][i]
    predCombined = data["pred_combined"][i]
    cTWorTWA = data["combined_uses_tw_twa"][i] * 200.0
    
    observationData[location][timestamp] = obs
    TWpredictionData[location][timestamp] = predTW
    TWApredictionData[location][timestamp] = predTWA
    CombinedpredictionData[location][timestamp] = predCombined
    CombinedTWorTWAData[location][timestamp] = cTWorTWA 
     
DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
 
week = 0
weekoftheday = 1
weeklyTimestamps = []
weeklyObservationData = {}
weeklyTWPredictionData = {}
weeklyTWAPredictionData = {}
weeklyCombinedPredictionData = {}
weeklycTWorTWAData = {}
     
for month in range(1, 13):
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
         
        weekoftheday = weekoftheday + 1
         
        if weekoftheday == 8 and week > 0:
            
            for location in locations:
                
                names = []
                names.append(stationNames[str(location)])
                names.append("TW")
                names.append("TWA")
                names.append("Combined")
                names.append("error (TW)")
                names.append("error (TWA)")
                names.append("error (Combined)")
                names.append("Combined TW/TWA")
                
                wData = []
                wData.append(weeklyObservationData[str(location)])
                wData.append(weeklyTWPredictionData[str(location)])
                wData.append(weeklyTWAPredictionData[str(location)])
                wData.append(weeklyCombinedPredictionData[str(location)])
                
                # generate errors
                obs = weeklyObservationData[str(location)]
                predTW = weeklyTWPredictionData[str(location)]
                predTWA = weeklyTWAPredictionData[str(location)]
                predCombined = weeklyCombinedPredictionData[str(location)]
                errorTW = []
                errorTWA = []
                errorCombined = []
                for i in range(0, len(obs)):
                    if math.isnan(obs[i]) or math.isnan(predTW[i]):
                        errorTW.append(float('nan'))
                    else:
                        errorTW.append(abs(predTW[i] - obs[i]))
                        
                    if math.isnan(obs[i]) or math.isnan(predTWA[i]):
                        errorTWA.append(float('nan'))
                    else:
                        errorTWA.append(abs(predTWA[i] - obs[i]))
                        
                    if math.isnan(obs[i]) or math.isnan(predCombined[i]):
                        errorCombined.append(float('nan'))
                    else:
                        errorCombined.append(abs(predCombined[i] - obs[i]))
                wData.append(errorTW)
                wData.append(errorTWA)
                wData.append(errorCombined)
                                
                wData.append(weeklycTWorTWAData[str(location)])
                
#                 doLineChart(OUTPUT_DIRECTORY + stationNames[str(location)].lower() + "_" + str(week) + "l.png", "No2 prediction - week " + str(week) + " @ " + stationNames[str(location)], "Hour of the week", "No2 level (ug/m3)", wData, names)
                
                for i in range(0, len(errorTW)):
                    if math.isnan(errorTW[i]) == False:
                        errorTW[i] = errorTW[i] * 5.0
                    if math.isnan(errorTWA[i]) == False:
                        errorTWA[i] = errorTWA[i] * 5.0
                    if math.isnan(errorCombined[i]) == False:
                        errorCombined[i] = errorCombined[i] * 5.0
                
                generateHeatmap(OUTPUT_DIRECTORY + stationNames[str(location)].lower() + "_" + str(week) + ".png", wData, "No2 heatmap - week " + str(week), names)
                generateColorHeatmap(OUTPUT_DIRECTORY + stationNames[str(location)].lower() + "_" + str(week) + "c.png", wData, "No2 heatmap - week " + str(week), names)                
                             
        if weekoftheday == 8:
            weekoftheday = 1
            week = week + 1
            weeklyTimestamps = []
            for loc in locations:
                weeklyObservationData[str(loc)] = []
                weeklyTWPredictionData[str(loc)] = []
                weeklyTWAPredictionData[str(loc)] = []               
                weeklyCombinedPredictionData[str(loc)] = []
                weeklycTWorTWAData[str(loc)] = []
             
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
             
            for loc in locations:
                if timestamp in observationData[str(loc)]:
                    weeklyObservationData[str(loc)].append(observationData[str(loc)][timestamp])
                else:
                    weeklyObservationData[str(loc)].append(float("nan"))
             
                if timestamp in TWpredictionData[str(loc)]:
                    weeklyTWPredictionData[str(loc)].append(TWpredictionData[str(loc)][timestamp])
                else:
                    weeklyTWPredictionData[str(loc)].append(float("nan"))
                    
                if timestamp in TWpredictionData[str(loc)]:
                    weeklyTWAPredictionData[str(loc)].append(TWApredictionData[str(loc)][timestamp])
                else:
                    weeklyTWAPredictionData[str(loc)].append(float("nan"))                    
                                 
                if timestamp in CombinedpredictionData[str(loc)]:
                    weeklyCombinedPredictionData[str(loc)].append(CombinedpredictionData[str(loc)][timestamp])
                else:
                    weeklyCombinedPredictionData[str(loc)].append(float("nan"))
                    
                if timestamp in CombinedTWorTWAData[str(loc)]: 
                    weeklycTWorTWAData[str(loc)].append(CombinedTWorTWAData[str(loc)][timestamp])
                else:
                    weeklycTWorTWAData[str(loc)].append(float("nan"))                    
                                        
