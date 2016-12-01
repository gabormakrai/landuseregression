import numpy as np
from matplotlib import pyplot as plt

def doGraph(data, title, xLabel, fileName):
    
    names = []
    
    for i in range(0, len(data)):
        names.append(str(i))
    
    index = np.arange(len(names))
    bar_width = 0.8
    
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.bar(index, data, bar_width, color='b', edgecolor='none')
    
    plt.xlabel(xLabel)
    plt.ylabel("#occurrence")
    plt.title(title)
     
    plt.margins(0.04, 0.04)
     
    plt.savefig(fileName)

def doGraph2(maxMae, data, title, xLabel, fileName):
            
    index = np.arange(-maxMae, maxMae + 1)
    bar_width = 0.8
    
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.bar(index, data, bar_width, color='b', edgecolor='none')
    
    plt.xlabel(xLabel)
    plt.ylabel("#occurrence")
    plt.title(title)
     
    plt.margins(0.04, 0.04)
     
    plt.savefig(fileName)

def doGraph3(data, title, xLabel, fileName):
        
    index = np.arange(0.0, 3.0, 0.01)
    bar_width = 0.01
    
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.bar(index, data, bar_width, color='b', edgecolor='none')
    
    plt.xlabel(xLabel)
    plt.ylabel("#occurrence")
    plt.title(title)
     
    plt.margins(0.04, 0.04)
     
    plt.savefig(fileName)
    
def doGraph4(data, title, xLabel, fileName):
        
    index = np.arange(-3.0, 3.0, 0.01)
    bar_width = 0.01
    
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.bar(index, data, bar_width, color='b', edgecolor='none')
    
    plt.xlabel(xLabel)
    plt.ylabel("#occurrence")
    plt.title(title)
     
    plt.margins(0.04, 0.04)
     
    plt.savefig(fileName)    
