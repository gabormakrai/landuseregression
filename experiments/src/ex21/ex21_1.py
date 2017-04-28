import matplotlib.pyplot as plt
from data.data import loadData
from numpy import median
from airquality import loadFile

DATA_FILE = "/media/sf_lur/data_london/data_hour_2015.csv"
OUTPUT_FILE1 = "/media/sf_lur/experiments/ex21/fig1.png"
OUTPUT_FILE2 = "/media/sf_lur/experiments/ex21/fig1_york.png"
DATA_DIRECTORY_YORK = "/media/sf_lur/data/aq/"

yorkStations = ["Fishergate", "Fulford", "Gillygate", "Heworth", "Lawrence"]
years = [2013]

yorkData = {}

print("Loading data...")

for station in yorkStations:
    yorkData[station] = []

for year in years:
    for i in range(0, len(yorkStations)):
        station = yorkStations[i]
        data = {}
        fileName = DATA_DIRECTORY_YORK + station + "_" + str(year) + ".csv"
        print("\tLoading data from " + fileName + "...")
        loadFile("no2", fileName, data)
        for timestampKey in data:
            yorkData[station].append(data[timestampKey])
        print("\tDone...")

print("Done...")

# load the data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

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

# for station in yorkStations:
#     stationNames.append(station)
#     stationData[station] = yorkData[station]

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

for station in yorkStations:
    stationNames.append(station)
    stationData[station] = yorkData[station]

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

plt.savefig(OUTPUT_FILE2)
