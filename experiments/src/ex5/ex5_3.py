import matplotlib.pyplot as plt
from data.data import loadData

OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex5/"

def plotError(fileName, column, targetColumn, data):
    
    # find out values
    values = set()
    for v in data[column]:
        values.add(v)
    
    namesNum = []
    for v in values:
        namesNum.append(v)
    
    namesNum.sort()
    
    names = []
    for n in namesNum:
        names.append(str(n))
    
    groupedData = {}
    
    # find out values2
    for i in range(0, len(data[targetColumn])):
        target = data[targetColumn][i]
        col = str(data[column][i])
        if col not in groupedData:
            groupedData[col] = []
        groupedData[col].append(target)
        
    dataToPlot = []
    for n in names:
        dataToPlot.append(groupedData[n])
    
    fig = plt.figure(None, figsize=(40, 40))
    ax = fig.add_subplot(111)
    
    ax.boxplot(dataToPlot, showfliers=False)
    ax.set_xticklabels(names, rotation='vertical')

    plt.savefig(fileName)

data = {}
columns = []
loadData(OUTPUT_DIRECTORY + "errors_rae.csv", [], data, columns)

targetColumn = "error_rae"

for c in columns:
    if c != targetColumn:
        plotError(OUTPUT_DIRECTORY + "rae_" + str(c) + ".png", c, targetColumn, data)
