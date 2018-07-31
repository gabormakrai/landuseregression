import matplotlib.pyplot as plt
from data.data import loadData

timestamps = ["20130724"]
stations = ["2.0"]

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

ATCData = {}

ATCData["20130724"] = {}
ATCData["20130724"]["2.0"] = [186,220,231,190,230,200,220,235,220,200,230,406,383,424,367,241,202,147,66]
ATCData["20130724"]["3.0"] = []
ATCData["20130724"]["4.0"] = [154,187,546,677,539,571,585,529,564,509,499,483,649,546,482,297,196,153,76]
ATCData["20130724"]["8.0"] = [153,107,339,379,300,291,324,315,352,332,379,239,246,315,226,204,220,177,94]

ATCData["20130827"] = {}
ATCData["20130827"]["2.0"] = [164,356,787,653,670,677,685,661,621,620,558,504,509,538,419,275,149,103,48]
ATCData["20130827"]["3.0"] = [171,157,281,381,321,288,253,276,285,263,277,309,394,330,246,239,146,139,83]
ATCData["20130827"]["4.0"] = [142,182,468,691,546,539,556,545,535,502,467,468,534,510,380,308,164,127,60]
ATCData["20130827"]["8.0"] = [136,124,286,367,329,299,331,308,391,403,426,410,464,303,261,224,184,118,60]

ATCData["20130924"] = {}
ATCData["20130924"]["2.0"] = [166,327,775,701,694,629,580,579,546,562,519,537,561,653,388,225,176,109,82]
ATCData["20130924"]["3.0"] = [205,134,371,509,321,253,275,262,258,257,344,360,464,407,324,241,166,124,86]
ATCData["20130924"]["4.0"] = [156,189,557,813,545,512,483,506,484,510,542,497,611,577,490,275,188,133,82]
ATCData["20130924"]["8.0"] = [144,132,361,433,322,322,311,341,358,397,447,413,382,360,269,202,231,126,93]

ATCData2 = {}

ATCData2["20130724"] = {}
ATCData2["20130724"]["2.0"] = [179,155,215,210,220,180,230,250,190,186,280,536,576,474,402,291,322,199,98]
ATCData2["20130724"]["3.0"] = []
ATCData2["20130724"]["4.0"] = [116,108,338,475,450,509,516,541,527,561,648,797,814,540,414,320,256,171,106]
ATCData2["20130724"]["8.0"] = [145,147,249,322,348,382,449,374,390,347,398,396,396,380,269,219,190,125,57]

ATCData2["20130827"] = {}
ATCData2["20130827"]["2.0"] = [169,181,332,407,442,489,503,514,602,619,755,845,822,623,403,363,232,146,81]
ATCData2["20130827"]["3.0"] = []
ATCData2["20130827"]["4.0"] = [132,109,335,460,404,452,513,591,522,545,513,725,724,516,360,337,192,142,83]
ATCData2["20130827"]["8.0"] = [144,156,277,389,410,421,461,452,388,396,358,363,364,341,265,204,173,93,49]

ATCData2["20130924"] = {}
ATCData2["20130924"]["2.0"] = [139,194,467,522,410,451,486,508,576,611,759,811,795,632,393,305,290,138,95]
ATCData2["20130924"]["3.0"] = [285,260,478,432,439,430,375,394,438,441,457,433,541,484,451,348,288,183,135]
ATCData2["20130924"]["4.0"] = [114,116,342,591,447,444,469,515,541,563,636,825,806,570,481,322,280,146,98]
ATCData2["20130924"]["8.0"] = [164,165,315,409,411,388,374,383,341,346,396,405,388,398,274,178,157,88,72]

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
#             ax2.spines["right"].set_position(("axes", y_axis_parameters[data_group_code][i]))
            make_patch_spines_invisible(ax2)
            ax2.spines["right"].set_visible(True)
            
        ax2.plot(index, X[i], '-', label=names[i], linewidth=1, color=colors[i])
        ax2.set_ylabel(names[i], color=colors[i])
        ax2.yaxis.label.set_color(colors[i])
        ax2.tick_params(axis='y', colors=colors[i])
    
    fig.subplots_adjust(right=0.85)
     
    plt.savefig(fileName)
    plt.close()    

for t in timestamps:
    for s in stations:
        original = ATCData[t][s]
        newArray = []
        for i in range(0,6):
            newArray.append(original[0]/6.0)
        for i in range(1,len(original)):
            newArray.append(original[i])
        ATCData[t][s] = newArray

for t in timestamps:
    for s in stations:
        original = ATCData2[t][s]
        newArray = []
        for i in range(0,6):
            newArray.append(original[0]/6.0)
        for i in range(1,len(original)):
            newArray.append(original[i])
        ATCData2[t][s] = newArray

OUTPUT_DIRECTORY = "/experiments/ex12/"

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
        for i in range(0,24):
            hour = ""
            if i < 10:
                hour = "0"
            hour = hour + str(i)
            hourlyTimestamps.append(timestamp + hour)
        
            
        columnsToUse = ["target"]
            
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
        
        if len(localData[0]) < 24:
            continue
                        
        avgAtcData = []
        for i in range(0, 24):
            atc1 = ATCData[timestamp][station][i]
            atc2 = ATCData2[timestamp][station][i]
            avgAtcData.append((atc1 + atc2) / 2.0)
            
        localData.append(avgAtcData)
        
        columnsToUse.append("atc (vehicle/hour)")
                
        fileName = OUTPUT_DIRECTORY + "ex12_" + stationName.lower() + "_" + timestamp + "_atc.png"
        graph(fileName, localData, localLabel, columnsToUse, stationName, "atc", timestamp)
            
        print(fileName)

