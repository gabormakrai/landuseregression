from data.data import loadData
from graph import graph

timestamps = ["20130724", "20130827", "20130924"]
stations = ["2.0", "3.0", "4.0", "5.0", "6.0", "7.0"]
dataCategories = ["lu", "td", "ts", "to", "we", "ti"]

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"
 
INPUT_DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex12/"

data = {}
columns = []
loadData(INPUT_DATA_FILE, [], data, columns)
    
for station in stations:
    stationName = stationNames[str(station)]
    print("Station " + stationName)
    
    for timestamp in timestamps:
        print("day: " + timestamp)
        
        #generate timestamps
        hourlyTimestamps = []
        for i in range(0,24):
            hour = ""
            if i < 10:
                hour = "0"
            hour = hour + str(i)
            hourlyTimestamps.append(timestamp + hour)
        
        for dc in dataCategories:
            print("dc:" + dc)
            
            columnsToUse = ["target"]
            
            if dc == "lu":
                columnsToUse.append('leisure_area')
                columnsToUse.append('landuse_area')
            if dc == "to":
                columnsToUse.append('buildings_number')
                columnsToUse.append('buildings_area')
            if dc == "ts":
                columnsToUse.append('lane_length')
                columnsToUse.append('length')
            if dc == "td":
                columnsToUse.append('traffic_length_car')
                columnsToUse.append('traffic_length_lgv')
                columnsToUse.append('traffic_length_hgv')
            if dc == "we":
                columnsToUse.append('winddirection')
                columnsToUse.append('windspeed')
                columnsToUse.append('temperature')
                columnsToUse.append('rain')
                columnsToUse.append('pressure')
            if dc == "ti":
                columnsToUse.append('hour')
                columnsToUse.append('day_of_week')
                columnsToUse.append('month')
                columnsToUse.append('bank_holiday')
                columnsToUse.append('race_day')
            
            localData = []
            for c in columnsToUse:
                localData.append([])
                
            localLabel = []
            for t in hourlyTimestamps:
                for i in range(0, len(data["timestamp"])):
                    if str(data["location"][i]) == station and str(int(data["timestamp"][i])) == t:
                        for j in range(0, len(columnsToUse)):
                            localData[j].append(data[columnsToUse[j]][i])
                        localLabel.append(t)
                        break
            
            print("localLabel: " + str(localLabel))
#             for i in range(0, len(localLabel)):
#                 print(localLabel[i])
#                 print(str(localData[i]))
                
            fileName = OUTPUT_DIRECTORY + stationName.lower() + "_" + timestamp + "_" + dc + ".png"
            
            graph(fileName, localData, localLabel, columnsToUse, "asd", "xAxis")
            
            print(fileName)
            #exit()
