from data.data import loadData
from ex11_lib import generateHeatmap
from ex11_lib import generateColorHeatmap

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex11/"

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

sNames = []
for loc in locations:
    sNames.append(stationNames[str(loc)])

# load data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)
 
observationData = {}
for loc in locations:
    observationData[str(loc)] = {}
 
for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    timestamp = str(int(data["timestamp"][i]))
    value = data["target"][i]    
    observationData[location][timestamp] = value
        
DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

week = 0
weekoftheday = 1
weeklyObservationData = {}
    
for month in range(1, 13):
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
        
        weekoftheday = weekoftheday + 1
        
        if weekoftheday == 8 and week > 0:
            wData = []
            for loc in locations:
                wData.append(weeklyObservationData[str(loc)])
            generateHeatmap(OUTPUT_DIRECTORY + "week_" + str(week) + ".png", wData, "No2 heatmap - week " + str(week), sNames)
            generateColorHeatmap(OUTPUT_DIRECTORY + "week_" + str(week) + "c.png", wData, "No2 heatmap - week " + str(week), sNames)
            
        if weekoftheday == 8:
            weekoftheday = 1
            week = week + 1
            for loc in locations:
                weeklyObservationData[str(loc)] = []
            
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
            
            for loc in locations:
                if timestamp in observationData[str(loc)]:
                    weeklyObservationData[str(loc)].append(observationData[str(loc)][timestamp])
                else:
                    weeklyObservationData[str(loc)].append(float("nan"))
                                
        