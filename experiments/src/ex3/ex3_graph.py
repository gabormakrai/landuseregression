import matplotlib.pyplot as plt

def loadData(fileName):
    data = {}
    
    print("Open file " + fileName + "...")
    
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
            
            # split the line
            splittedLine = line.split(',')
            
            group = str(splittedLine[0])
            
            if group not in data:
                data[group] = []
                
            data[group].append(float(splittedLine[1]))
            
    print("Done...")
    
    return data
            
inputFile = "/media/sf_lur/experiments/ex3/result_rfr.csv"
outputFile1 = "/media/sf_lur/experiments/ex3/graph_rfr_1.png"
outputFile2 = "/media/sf_lur/experiments/ex3/graph_rfr_2.png"
outputFile3 = "/media/sf_lur/experiments/ex3/graph_rfr_3.png"

data = loadData(inputFile)

fig = plt.figure(1, figsize=(40, 20))
ax = fig.add_subplot(111)

dataToPlot = []

groups = []

for group in data:
    groups.append(group)
    
groups.sort()

for group in groups:
    groupData = data[group]
    zero = False
    for i in range(0, len(groupData)):
        if groupData[i] > 300.0:
            zero = True
    if zero:
        for i in range(0, len(groupData)):
            groupData[i] = 0.0
    
    dataToPlot.append(groupData)
    print(str(group) + " -> " + str(len(groupData)))


ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(groups, rotation='vertical')
plt.ylim(0.0, 30.0)

plt.savefig(outputFile1)

fig = plt.figure(2, figsize=(8, 8))
ax = fig.add_subplot(111)

dataWithoutTimeWeather = []
dataWithTime = []
dataWithWeather = []
dataWithTimeWeather = []

for group in groups:
    groupData = data[group]
    zero = False
    for i in range(0, len(groupData)):
        if groupData[i] > 300.0:
            zero = True
    if zero:
        for i in range(0, len(groupData)):
            groupData[i] = 0.0
            
    for v in groupData:
        if "we0ti0" in group:
            dataWithoutTimeWeather.append(v)
        elif "we1ti0" in group:
            dataWithWeather.append(v)
        elif "we0ti1" in group:
            dataWithTime.append(v)
        else:
            dataWithTimeWeather.append(v)
            
print("dataWithoutTimeWeather: " + str(len(dataWithoutTimeWeather)))
print("dataWithWeather: " + str(len(dataWithWeather)))
print("dataWithTime: " + str(len(dataWithTime)))
print("dataWithTimeWeather: " + str(len(dataWithTimeWeather)))

ax.boxplot([dataWithoutTimeWeather, dataWithWeather, dataWithTime, dataWithTimeWeather], showfliers=False)
ax.set_xticklabels(["w/o T, w/o W", "w/ W", "w/ T", "w/ T+W"] )
plt.ylim(0.0, 30.0)
plt.ylabel("RMSE (ug/m3)")

plt.savefig(outputFile2)

fig = plt.figure(3, figsize=(13, 13))
ax = fig.add_subplot(111)

referenceData = data["lu0to0ts0td0we1ti1"]
dataToPlot = []
groupNames = []

for group in groups:
    groupData = data[group]
    zero = False
    for i in range(0, len(groupData)):
        if groupData[i] > 300.0:
            zero = True
    if zero:
        for i in range(0, len(groupData)):
            groupData[i] = 0.0
            
    if group == "lu0to0ts0td0we1ti1":
        continue
    
    if "we1ti1" not in group:
        continue
    
    groupNames.append(group[0:12])
    for i in range(0, len(groupData)):
        groupData[i] = 1.0 + (groupData[i] - referenceData[i]) / referenceData[i]

    dataToPlot.append(groupData)
        
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(groupNames, rotation='vertical')
plt.ylim(0.0, 2.0)
plt.ylabel("Relative error to only (T+W) result")
plt.savefig(outputFile3)


