from data.data import loadData
from graph import doScatterChart

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex9/"

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
 
observationData = {}
for loc in stationNames:
    observationData[str(loc)] = {}
 
for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    timestamp = str(int(data["timestamp"][i]))
    value = data["target"][i]    
    observationData[location][timestamp] = value
    
DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

for s1 in stationNames:
    for s2 in stationNames:
        if s1 == s2:
            continue

        X = []
        Y = []
        Y2 = []
        
        for month in range(1, 13):
            for day in range(1, DAYS_OF_MONTH[month - 1] + 1):        
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
                    
                    if timestamp in observationData[s1] and timestamp in observationData[s2]:
                        x = observationData[s1][timestamp]
                        y = observationData[s2][timestamp]
                        if x > 0.00001 and y / x < 5.0:
                            X.append(x)
                            Y.append(y / x)
                            Y2.append(y)
        fileName = OUTPUT_DIRECTORY + "r_" + stationNames[s1].lower() + "_" + stationNames[s2].lower()
        fileName2 = OUTPUT_DIRECTORY + "g_" + stationNames[s1].lower() + "_" + stationNames[s2].lower()
        title = "Observations " + stationNames[s1] + " - " + stationNames[s2]
        xAxis = "ug/m3 @ " + stationNames[s1]
        yAxis = "relative ug/m3 @ " + stationNames[s2]
        y2Axis = "ug/m3 @ " + stationNames[s2]
        
        doScatterChart(fileName, title, xAxis, yAxis, X, Y)            
        doScatterChart(fileName2, title, xAxis, y2Axis, X, Y2)            
