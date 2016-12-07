import matplotlib.pyplot as plt

def generateTimestampsForADay(dayTimestamp):
    
    ts = []
    
    for hour in range(0, 24):
        if hour < 10:
            timestamp = dayTimestamp + "0" + str(hour)
        else:
            timestamp = dayTimestamp + str(hour)
        ts.append(timestamp)
    
    return ts

def doLineChart(fileName, title, data, names, data2, names2, data3, names3):
            
    index = []
    for i in range(0, 24):
        index.append(i)
        
    fig = plt.figure(None, figsize=(12, 10))
    ax = fig.add_subplot(311)
    
    for i in range(0, len(data)):
        ax.plot(index, data[i], '-', label=names[i])
     
#    plt.xlabel(xAxis)
    plt.ylabel("conc. level (ug/m3)")
    plt.title(title)
    plt.margins(0.04, 0.04)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    ax = fig.add_subplot(312)
    
    for i in range(0, len(data2)):
        ax.plot(index, data2[i], '-', label=names2[i])
    
    plt.ylabel("error level (ug/m3)")
    plt.margins(0.04, 0.04)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    ax = fig.add_subplot(313)
    
    for i in range(0, len(data3)):
        if i < 7:
            ax.plot(index, data3[i], '-', label=names3[i])
        else:
            ax.plot(index, data3[i], '--', label=names3[i])
    
    plt.ylabel("normalized value")
    plt.xlabel("hour of the day")
    lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
         
    plt.margins(0.04, 0.04)
 
    plt.savefig(fileName, bbox_extra_artists=(lgd,), bbox_inches='tight')
    
def doBoxplot(fileName, title, yAxis, data, names):
    
    fig = plt.figure(None, figsize=(10, 10))
    
    ax = fig.add_subplot(111)

    ax.boxplot(data) # , showfliers=False)
    
    ax.set_xticklabels(names) #, rotation='vertical')
    
    plt.ylabel(yAxis)
    
    plt.savefig(fileName)
    