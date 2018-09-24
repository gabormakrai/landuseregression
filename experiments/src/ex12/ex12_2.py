from matplotlib import pyplot as plt
from data.data import loadData

OUTPUT_DIRECTORY = "/experiments/ex12/"

timestamps = ["20130724", "20130827", "20130924"]
stations = ["2.0", "3.0", "4.0", "5.0", "6.0", "7.0"]
dataCategories = ["we1", "we2", "we3", "ti1", "ti2", "ti3", "lu", "td1", "td2", "td3", "ts", "to"]
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
    "td1": 0.75, 
    "td2": 0.75, 
    "td3": 0.75, 
    "ts": 0.75, 
    "to": 0.75, 
    "we1": 0.75, 
    "we2": 0.75, 
    "we3": 0.75, 
    "ti1": 0.75,
    "ti2": 0.75,
    "ti3": 0.75
}

y_axis_parameters = {
    "lu": [None, None, 1.2],
    "td1": [None, None],
    "td2": [None, None],
    "td3": [None, None],
    "ts": [None, None, 1.2],
    "to": [None, None, 1.2],
    "we1": [None, None, 1.2],
    "we2": [None, None, 1.2],
    "we3": [None, None],
    "ti1": [None, None, 1.2],
    "ti2": [None, None, 1.2],
    "ti3": [None, None],
}

y_axis_labelpad = {
    "lu": [None, -5, 0],
    "td1": [None, 0],
    "td2": [None, 0],
    "td3": [None, 0],
    "ts": [None, 3, 3],
    "to": [None, 2, 4],
    "we1": [None, 0, 0],
    "we2": [None, 0, 0],
    "we3": [None, 0],
    "ti1": [None, 0, 0],
    "ti2": [None, 0, 0],
    "ti3": [None, 0]
}

limits = {
    "lu": [None, [-0.1, 0.5], [-0.1, 1.0]],
    "td1": [None, None],
    "td2": [None, None],
    "td3": [None, None],
    "ts": [None, None, [160, 200]],
    "to": [None, None, [0.0, 0.5]],
    "we1": [None, None, None],
    "we2": [None, None, None],
    "we3": [None, None],
    "ti1": [None, None, None],
    "ti2": [None, None, None],
    "ti3": [None, None]
}
 
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def graph(fileName, X, xLabel, names, stationName, data_group_code, day_string):
    
    colors = ['r', 'g', 'b', 'y', 'c', 'gray']
    index = range(0, len(xLabel))
        
    fig = plt.figure(figsize=(5.76*0.8, 5.76*0.8))
    
    ax = fig.add_subplot(111)
    ax.plot(index, X[0], '-', label=names[0], linewidth=1, color=colors[0])
    ax.set_ylabel("Observation @ " + stationName + r' ($\mu$gm${}^{-3}$)', color=colors[0])
    ax.set_xlabel("Hour of the day (" + day_string + ")")
    ax.yaxis.label.set_color(colors[0])
    ax.tick_params(axis='y', colors=colors[0])
    print(str(len(X[0])))
    
    if data_group_code == "td":
        for i in range(1, len(X)):
            X[i] = [X[i][j] / 1000.0 for j in range(0, len(X[i]))]
        names = [n + r'$ (10^{3})$' for n in names]
        
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
            if dc == "td1":
                columnsToUse.append('traffic_length_car')
            if dc == "td2":
                columnsToUse.append('traffic_length_lgv')
            if dc == "td3":
                columnsToUse.append('traffic_length_hgv')
            if dc == "we1":
                columnsToUse.append('winddirection')
                columnsToUse.append('windspeed')
            if dc == "we2":
                columnsToUse.append('temperature')
                columnsToUse.append('rain')
            if dc == "we3":
                columnsToUse.append('pressure')
            if dc == "ti1":
                columnsToUse.append('hour')
                columnsToUse.append('day_of_week')
            if dc == "ti2":
                columnsToUse.append('month')
                columnsToUse.append('bank_holiday')
            if dc == "ti3":
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
            
