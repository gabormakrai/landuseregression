from matplotlib import pyplot as plt
from data.data import loadData

OUTPUT_DIRECTORY = "/experiments/ex12/"

timestamps = ["20130724", "20130827", "20130924"]
stations = ["2.0", "3.0", "4.0", "5.0", "6.0", "7.0"]
dataCategories = ["lu", "td", "ts", "to", "we", "ti"]

timestamps = ["20130724"]
stations = ["2.0"]

stationNames = {
    "2.0": "Fulford", 
    "3.0": "Gillygate", 
    "4.0": "Heworth",
    "5.0": "Holgate",
    "6.0": "Lawrence",
    "7.0": "Nunnery",
    "8.0": "Fishergate"
}

right_border = {
    "lu": 0.75,
    "td": 0.65, 
    "ts": 0.75, 
    "to": 0.75, 
    "we": 0.7, 
    "ti": 0.7
}

y_axis_parameters = {
    "lu": [None, None, 1.2],
    "td": [None, None, 1.22, 1.48],
    "ts": [None, None, 1.2],
    "to": [None, None, 1.2],
    "we": [None, None, 1.095, 1.16, 1.235, 1.32],
    "ti": [None, None, 1.08, 1.16, 1.25, 1.35]
}

y_axis_labelpad = {
    "lu": [None, -5, 0],
    "td": [None, 0, 3, -3],
    "ts": [None, 3, 3],
    "to": [None, 2, 4],
    "we": [None, 0, -5, -1, -5, 0],
    "ti": [None, 0, 2, 1, 0, 0]
}

limits = {
    "lu": [None, [-0.1, 0.5], [-0.1, 1.0]],
    "td": [None, None, None, None],
    "ts": [None, None, [160, 200]],
    "to": [None, None, [0.0, 0.5]],
    "we": [None, None, None, None, [-0.1, 1.2], None],
    "ti": [None, None, [-0.1, 6.2], [-0.1, 11.1], [-0.1, 1.1], [-0.2, 1.3]]
}
 
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def graph(fileName, X, xLabel, names, stationName, data_group_code, day_string):
    
    colors = ['r', 'g', 'b', 'y', 'c', 'gray']
    index = range(0, len(xLabel))
        
    if data_group_code == "we" or data_group_code == "ti":
        fig = plt.figure(figsize=(5.76*1.5, 5.76*1.5))
    else:
        fig = plt.figure(figsize=(5.76*0.8, 5.76*0.8))
    
    ax = fig.add_subplot(111)
    ax.plot(index, X[0], '-', label=names[0], linewidth=1, color=colors[0])
    ax.set_ylabel("Observation @ " + stationName + " (ug/m3)", color=colors[0])
    ax.set_xlabel("Hour of the day (" + day_string + ")")
    ax.yaxis.label.set_color(colors[0])
    ax.tick_params(axis='y', colors=colors[0])
    print(str(len(X[0])))
    
    if data_group_code == "td":
        for i in range(1, len(X)):
            X[i] = [X[i][j] / 1000.0 for j in range(0, len(X[i]))]
        names = [n + " (10^3)" for n in names]
        
    for i in range(1, len(X)):
        print(str(len(X[i])))
        ax2 = ax.twinx()
        if i > 1:
            ax2.spines["right"].set_position(("axes", y_axis_parameters[data_group_code][i]))
            make_patch_spines_invisible(ax2)
            ax2.spines["right"].set_visible(True)
            
        ax2.plot(index, X[i], '-', label=names[i], linewidth=1, color=colors[i])
        ax2.set_ylabel(names[i], color=colors[i])
        ax2.yaxis.label.set_color(colors[i])
        ax2.yaxis.labelpad = y_axis_labelpad[data_group_code][i]
        ax2.tick_params(axis='y', colors=colors[i])
        if limits[data_group_code][i] != None: 
            ax2.set_ylim(limits[data_group_code][i][0], limits[data_group_code][i][1])   
    
#     plt.ylim(ymin=-1)
    if data_group_code == "we" or data_group_code == "ti":
        fig.subplots_adjust(right=right_border[data_group_code], left=0.075)
    else:
        fig.subplots_adjust(right=right_border[data_group_code], left=0.12)
     
    plt.savefig(fileName)
    plt.close()    

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", [], data, columns)
    
for station in stations:
    stationName = stationNames[str(station)]
    print("Station " + stationName)
    
    for timestamp in timestamps:
        print("day: " + timestamp)
        
        #generate timestamps
        hourlyTimestamps = []
        for i in range(0, 24):
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
                
            fileName = OUTPUT_DIRECTORY + "ex12_" + stationName.lower() + "_" + timestamp + "_" + dc + ".png"
            
            graph(fileName, localData, localLabel, columnsToUse, stationName, dc, timestamp)
            
            print(fileName)
            
