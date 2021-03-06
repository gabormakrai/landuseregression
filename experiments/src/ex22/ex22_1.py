import matplotlib.pyplot as plt
from data.data import loadData
from numpy import median

DATA_FILE1 = "/data/london3_hour_2015.csv"
OUTPUT_FILE1 = "/experiments/ex22/ex22_1.png"

# load the data
data = {}
columns = []
loadData(DATA_FILE1, [], data, columns)

# get the observation data for each station

stationData = {}
stationNames = []
for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    value = data["target"][i]
    if location not in stationData:
        stationNames.append(location)
        stationData[location] = []
    stationData[location].append(value)

stationNames = sorted(stationNames)

l = []
for station in stationNames:
    l.append((station, median(stationData[station])) )

medianSortedStationNames = sorted(l, key=lambda tup: tup[1])

fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)

stationNames = []
dataToPlot = []
for tup in medianSortedStationNames:
    stationNames.append(tup[0])
    dataToPlot.append(stationData[tup[0]])

print("Stations in median sorted order:")
print(str(stationNames))

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(stationNames, rotation='vertical')

plt.ylabel("Concentration levels (ug/m3)")
plt.ylim(-5.0, 400.0)

plt.savefig(OUTPUT_FILE1)
