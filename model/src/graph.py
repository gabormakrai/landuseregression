import numpy as np
import matplotlib.pyplot as plt

def doErrorBar(fileName, title, xAxis, yAxis, names, means, stddevs):
    
    plt.subplots()

    index = np.arange(len(names))

    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    plt.bar(index, means, bar_width,
        alpha=opacity,
        color='b',
        yerr=stddevs,
        error_kw=error_config)
    
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
    plt.xticks(index + (bar_width / 2), names)
    
    plt.margins(0.04, 0.04)

    plt.savefig(fileName)

