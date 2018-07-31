import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def doLineChart(fileName, title, xAxis, yAxis, data, names):
    
    colors = []
    
    for i in range(0, 256):
        c = hex(i).split('x')[-1]
        if len(c) == 1:
            c = "0" + c
        colors.append("#" + c + "ff00")
        
    for i in range(0, 256):
        c = hex(255 - i).split('x')[-1]
        if len(c) == 1:
            c = "0" + c
        colors.append("#ff" + c + "00")
    
    index = []
    for i in range(0, len(names)):
        index.append(i)
        
    fig = plt.figure(None, figsize=(20, 14))
    ax = fig.add_subplot(111)
        
    for i in range(0, len(data)):
        ax.plot(index, data[i], '-', color=colors[i*14])
    
    ax.set_xticks(np.arange(len(names)))
    ax.set_xticklabels([str(int(float(name))) for name in names])
     
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.margins(0.04, 0.04)
    
    plt.savefig(fileName)

def loadEx24Data(fileName):
    stations = []
    data = defaultdict(lambda: defaultdict(list))

    firstLine = True
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:                
            # remove newline character from the end
            line = line.rstrip()
            
            # parse header
            if firstLine == True:
                firstLine = False
                continue
            splittedLine = line.split(",")
            
            trainStation = splittedLine[0]
            testStation = splittedLine[1]
            rmse = float(splittedLine[2])
            
            if trainStation not in stations:
                stations.append(trainStation)
            data[trainStation][testStation] = rmse
    return stations, data

DATA_FILE_TW = "/experiments/ex29/ex29_5_tw.csv"
DATA_FILE_TWA = "/experiments/ex29/ex29_5_twa.csv"
DATA_FILE_ALL = "/experiments/ex29/ex29_5_all.csv"

OUTPUT_FILE_TW = "/experiments/ex29/ex29_5_tw.png"
OUTPUT_FILE_TWA = "/experiments/ex29/ex29_5_twa.png"
OUTPUT_FILE_ALL = "/experiments/ex29/ex29_5_all.png"

def doOne(inputFile, outputFile):

    stations, data = loadEx24Data(inputFile)
    
    print(str(stations))
    
    dataToPlot = []
    for station in stations:
        stationData = []
        for s in stations:
            stationData.append(data[station][s])
        dataToPlot.append(stationData)
    
    doLineChart(
        outputFile, 
        "Prediction accuracy of models trained on 1 station data", 
        "Test Station", 
        "RMSE (ug/m3)", 
        dataToPlot, 
        stations)

doOne(DATA_FILE_TW, OUTPUT_FILE_TW)
doOne(DATA_FILE_TWA, OUTPUT_FILE_TWA)
doOne(DATA_FILE_ALL, OUTPUT_FILE_ALL)