import matplotlib.pyplot as plt

def doScatterChart(fileName, title, xAxis, yAxis, x, y):
                    
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    
    ax.scatter(x, y, c='r', alpha=0.1)
         
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
    ax.legend()
    
#     plt.xticks(index + (0.5 / 2), names)
     
    plt.margins(0.04, 0.04)
 
    plt.savefig(fileName)

