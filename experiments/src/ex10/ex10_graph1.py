import matplotlib.pyplot as plt

def loadData(fileName):
    dataDayNight = {}
    dataNightDay = {}
    
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
            
            dayNight = str(splittedLine[0])
            group = str(splittedLine[1])
            
            if dayNight == "True":
                if group not in dataDayNight:
                    dataDayNight[group] = []
                dataDayNight[group].append(float(splittedLine[2]))
            else:
                if group not in dataNightDay:
                    dataNightDay[group] = []
                dataNightDay[group].append(float(splittedLine[2]))
            
    print("Done...")
    
    return dataDayNight, dataNightDay
            
inputFile = "/media/sf_lur/experiments/ex10/result_rfr.csv"
outputFile1 = "/media/sf_lur/experiments/ex10/graph_rfr_daynight.png"

dataDayNight, dataNightDay = loadData(inputFile)

fig = plt.figure(None, figsize=(40, 20))
ax = fig.add_subplot(111)

dataToPlot = []

groups = []

for group in dataDayNight:
    groups.append(group)
    
groups.sort()

for group in groups:
    groupData = dataDayNight[group]
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
#plt.ylim(0.0, 30.0)

plt.savefig(outputFile1)

inputFile = "/media/sf_lur/experiments/ex10/result_rfr.csv"
outputFile1 = "/media/sf_lur/experiments/ex10/graph_rfr_nightday.png"

dataDayNight, dataNightDay = loadData(inputFile)

fig = plt.figure(None, figsize=(40, 20))
ax = fig.add_subplot(111)

dataToPlot = []

groups = []

for group in dataNightDay:
    groups.append(group)
    
groups.sort()

for group in groups:
    groupData = dataNightDay[group]
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
#plt.ylim(0.0, 30.0)
plt.ylabel("RMSE (ug/m3)") 
plt.savefig(outputFile1)

dataToPlot = {}
# lu1to1ts1td1we1ti1
for g in ["lu", "to", "ts", "td", "we", "ti"]:
    dataToPlot[g + "0_daynight"] = []
    dataToPlot[g + "1_daynight"] = []
    dataToPlot[g + "0_nightday"] = []
    dataToPlot[g + "1_nightday"] = []

for group in groups:
    groupDataDayNight = dataDayNight[group]
    groupDataNightDay = dataNightDay[group]
            
    # lu1to1ts1td1we1ti1
    if "lu1" in group:
        for v in groupDataDayNight:
            dataToPlot["lu1_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["lu1_nightday"].append(v);
    else:
        for v in groupDataDayNight:
            dataToPlot["lu0_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["lu0_nightday"].append(v);
                 
    # lu1to1ts1td1we1ti1
    if "to1" in group:
        for v in groupDataDayNight:
            dataToPlot["to1_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["to1_nightday"].append(v);
    else:
        for v in groupDataDayNight:
            dataToPlot["to0_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["to0_nightday"].append(v);
            
    # lu1to1ts1td1we1ti1
    if "ts1" in group:
        for v in groupDataDayNight:
            dataToPlot["ts1_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["ts1_nightday"].append(v);
    else:
        for v in groupDataDayNight:
            dataToPlot["ts0_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["ts0_nightday"].append(v);
            
    # lu1to1ts1td1we1ti1
    if "td1" in group:
        for v in groupDataDayNight:
            dataToPlot["td1_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["td1_nightday"].append(v);
    else:
        for v in groupDataDayNight:
            dataToPlot["td0_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["td0_nightday"].append(v);

    # lu1to1ts1td1we1ti1
    if "we1" in group:
        for v in groupDataDayNight:
            dataToPlot["we1_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["we1_nightday"].append(v);
    else:
        for v in groupDataDayNight:
            dataToPlot["we0_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["we0_nightday"].append(v);

    # lu1to1ts1td1we1ti1
    if "ti1" in group:
        for v in groupDataDayNight:
            dataToPlot["ti1_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["ti1_nightday"].append(v);
    else:
        for v in groupDataDayNight:
            dataToPlot["ti0_daynight"].append(v);
        for v in groupDataNightDay:
            dataToPlot["ti0_nightday"].append(v);
            
# lu1to1ts1td1we1ti1
# dc = DataCategory
for dC in ["lu", "to", "ts", "td", "we", "ti"]:
    fig = plt.figure(None, figsize=(20, 10))
    ax = fig.add_subplot(111)

    outputFile2 = "/media/sf_lur/experiments/ex10/graph1_" + dC + ".png"
    dataToPlot2 = []
    for g in [dC + "0_daynight", dC + "1_daynight", dC + "0_nightday", dC + "1_nightday"]:
        dataToPlot2.append(dataToPlot[g])
                
    ax.boxplot(dataToPlot2, showfliers=False)
    ax.set_xticklabels(["w/o " + dC.upper() + " @ dayNight", "w/ " + dC.upper() + " @ dayNight", "w/o " + dC.upper() + " @ nightDay", "w/ " + dC.upper() + " @ nightDay"] )
    plt.ylabel("RMSE (ug/m3)") 
    plt.savefig(outputFile2)

# reordered first graph
for dC in ["lu", "to", "ts", "td", "we", "ti"]:
    
    groups2 = []
    for g in groups:
        if dC + "0" in g:
            groups2.append(g)
    for g in groups:
        if dC + "1" in g:
            groups2.append(g)

    outputFile2DN = "/media/sf_lur/experiments/ex10/graph2_" + dC + "_daynight.png"
    outputFile2ND = "/media/sf_lur/experiments/ex10/graph2_" + dC + "_nightday.png"
    dataToPlotDN = []
    dataToPlotND = []
    
    for group in groups2:
        groupDataND = dataNightDay[group]
        groupDataDN = dataDayNight[group]        
        dataToPlotND.append(groupDataND)
        dataToPlotDN.append(groupDataDN)
                
    fig = plt.figure(None, figsize=(30, 20))
    ax = fig.add_subplot(111)
    ax.boxplot(dataToPlotDN, showfliers=False)
    ax.set_xticklabels(groups2, rotation='vertical')
    plt.ylabel("RMSE (ug/m3)") 
    plt.savefig(outputFile2DN)

    fig = plt.figure(None, figsize=(30, 20))
    ax = fig.add_subplot(111)
    ax.boxplot(dataToPlotND, showfliers=False)
    ax.set_xticklabels(groups2, rotation='vertical')
    plt.ylabel("RMSE (ug/m3)") 
    plt.savefig(outputFile2ND)

