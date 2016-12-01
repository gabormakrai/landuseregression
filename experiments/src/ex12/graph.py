import numpy as np
from matplotlib import pyplot as plt

def graph(fileName, X, xLabel, names, title, xAxis):
    
    colors = ['r', 'g', 'b', 'y', 'c', 'gray']
        
    index = []
    for i in range(0, len(xLabel)):
        index.append(i)
        
    fig = plt.figure(None, figsize=(10, 10))
    
    ax = fig.add_subplot(111)
    ax.plot(index, X[0], '-', label=names[0], linewidth=2, color=colors[0])
    ax.set_ylabel(names[0], color=colors[0])
    ax.yaxis.label.set_color(colors[0])
    ax.tick_params(axis='y', colors=colors[0])
    print(str(len(X[0])))
        
    for i in range(1, len(X)):
        print(str(len(X[i])))
        ax2 = ax.twinx()
        ax2.plot(index, X[i], '-', label=names[i], linewidth=2, color=colors[i])
        ax2.set_ylabel(names[i], color=colors[i])
        ax2.yaxis.label.set_color(colors[i])
        ax2.tick_params(axis='y', colors=colors[i])     
    
    plt.ylim(ymin=-1)
    plt.title(title)
     
    plt.savefig(fileName)    
