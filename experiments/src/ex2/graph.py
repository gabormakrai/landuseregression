import numpy as np
import matplotlib.pyplot as plt

def doBarChart(fileName, title, xAxis, yAxis, names, values):
    
    fig = plt.figure(None)
    
    index = np.arange(len(names))
    
    x = []
    for i in range(0, len(names)):
        x.append(i)
    
    ax = fig.add_subplot(111)
    
    ax.bar(x, values, 0.5)
    
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
    plt.xticks(index + (0.5 / 2), names)
    
    plt.margins(0.04, 0.04)

    plt.savefig(fileName)
