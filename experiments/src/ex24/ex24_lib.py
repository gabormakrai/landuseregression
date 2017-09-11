import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def doLineChart(fileName, title, xAxis, yAxis, data, names):
    
    colors = []
    for i in range(0,100):
        c = hex(56 + 5 * i).split('x')[-1]
        color = "#" + c + c + c
        colors.append(color)
    
    index = []
    for i in range(0, len(names)):
        index.append(i)
        
    fig = plt.figure(None, figsize=(30, 10))
    ax = fig.add_subplot(111)
    ax.set_facecolor('blue')
        
    for i in range(0, len(data)):
        ax.plot(index, data[i], '-', color=colors[i])
    
    ax.set_xticks(np.arange(len(names)))
    ax.set_xticklabels([str(int(float(name))) for name in names])
     
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
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
