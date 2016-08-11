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

def doScatterDiagram(fileName, title, xAxis, yAxis, x, y):
    
    plt.subplots()
        
    plt.scatter(x, y, c='r', alpha=0.1)
    
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
    plt.margins(0.04, 0.04)
    
#     plt.xlim(-20.0, 300.0)
#     plt.ylim(-20.0, 300.0)
    plt.xlim(0.0, 150.0)
    plt.ylim(0.0, 100.0)
        
    plt.savefig(fileName)

def doHourlyErrorBar(fileName, title, xAxis, yAxis, names, result, colors):
    
    N = len(result[names[0]])
    ind = np.arange(N)
    width = 0.14

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    rectangles = []
    
    for i in range(0, len(names)):
        name = names[i]
        rects = ax.bar(ind + i * width, result[name], width, color=colors[name])
        rectangles.append(rects)
    
    ax.set_ylabel(yAxis)
    ax.set_xlabel(xAxis)
    ax.set_xticks(ind+width)
    labels = range(0, N)
    ax.set_xticklabels( labels )
    legend1 = []
    for rectangle in rectangles:#     nmse1 = nmse
        legend1.append(rectangle[0])
#    ax.legend( (rectangles[0][0], rectangles[1][0], rectangles[2][0]), ('y', 'z', 'k') )
    ax.legend( legend1, names,loc='best',prop={'size':6} )

    def autolabel(rects):
        for rect in rects:
            rect.get_height()
#            h = rect.get_height()
#            ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h), ha='center', va='bottom')

    for rect in rectangles:
        autolabel(rect)

#     autolabel(rects1)
#     autolabel(rects2)
#     autolabel(rects3)

    plt.title(title)    
    plt.margins(0.04, 0.04)
    
    plt.savefig(fileName)
