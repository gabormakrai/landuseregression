import matplotlib.pyplot as plt

INPUT_DATA_FILE = "/experiments/ex3/ex3_1.csv"
OUTPUT_FILE_1 = "/experiments/ex3/ex3_1.png"
OUTPUT_FILE_2 = "/experiments/ex3/ex3_2.png"
OUTPUT_FILE_3 = "/experiments/ex3/ex3_3.png"

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
            
data = loadData(INPUT_DATA_FILE)

fig = plt.figure(figsize=(9.36*1.5, 5.76*1.5))
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

x = [i for i in range(0, len(dataToPlot))]
ax.plot(x, dataToPlot)
ax.set_xticks(x)

groups_names = [s.replace("lu", "L") for s in groups]
groups_names = [s.replace("we", "W") for s in groups_names]
groups_names = [s.replace("ti", "T") for s in groups_names]
groups_names = [s.replace("td", "V") for s in groups_names]
groups_names = [s.replace("ts", "R") for s in groups_names]
groups_names = [s.replace("to", "B") for s in groups_names]

ax.set_xticklabels(groups_names, rotation='vertical')
plt.ylim(10.0, 22.0)
plt.ylabel("RMSE (ug/m3)")
plt.xlabel("Data sources")

fig.subplots_adjust(bottom=0.2)

plt.savefig(OUTPUT_FILE_1)
plt.close()

fig = plt.figure(figsize=(9.36, 5.76))
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
 
ax.boxplot([dataWithoutTimeWeather, dataWithTime, dataWithWeather, dataWithTimeWeather], showfliers=False)
ax.set_xticklabels(["w/o T, w/o W", "w/ T", "w/ W", "w/ T+W"] )
plt.ylim(10.0, 22.0)
plt.ylabel("RMSE (ug/m3)")
plt.xlabel("Data sources")
 
plt.savefig(OUTPUT_FILE_2)
plt.close()
 
fig = plt.figure(figsize=(9.36, 5.76))
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
         
# ax.boxplot(dataToPlot, showfliers=False)
# ax.set_xticklabels(groupNames, rotation='vertical')
# plt.savefig(OUTPUT_FILE_3)

x = [i for i in range(0, len(dataToPlot))]
ax.plot(x, dataToPlot)
ax.set_xticks(x)

groups_names = [s.replace("lu", "L") for s in groupNames]
groups_names = [s.replace("we", "W") for s in groups_names]
groups_names = [s.replace("ti", "T") for s in groups_names]
groups_names = [s.replace("td", "V") for s in groups_names]
groups_names = [s.replace("ts", "R") for s in groups_names]
groups_names = [s.replace("to", "B") for s in groups_names]

ax.set_xticklabels(groups_names, rotation='vertical')
plt.ylim(0.9, 1.35)
plt.ylabel("Relative RMSE to only (T+W) result")
plt.xlabel("Additional data sources to (T+W)")

fig.subplots_adjust(bottom=0.2)

plt.savefig(OUTPUT_FILE_3)
plt.close()

