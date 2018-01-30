import matplotlib.pyplot as plt
from data.data import loadData
from numpy import median

DATA_FILE = "/data/london3_hour_2016.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_1.png"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_1.txt"

output_log = open(OUTPUT_LOG_FILE, "w")

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

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

stationNames = sorted(stationNames)

l = []
for station in stationNames:
    l.append((station, median(stationData[station])) )

medianSortedStationNames = sorted(l, key=lambda tup: tup[1])

fig = plt.figure(figsize=(9.36*1.3, 5.76*1.3))
ax = fig.add_subplot(111)

stationNames = []
stationNames2 = []

dataToPlot = []
for tup in medianSortedStationNames:
    stationNames2.append(tup[0])
    stationNames.append(str(int(float(tup[0]))) + " (" + str(len(stationData[tup[0]])) + ")")
    dataToPlot.append(stationData[tup[0]])

log("Stations in median sorted order:")
log(str(stationNames2))

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(stationNames, rotation='vertical')

fig.subplots_adjust(right=0.95, left=0.075, bottom=0.15, top=0.95)

plt.ylabel("Concentration levels (ug/m3)")
plt.ylim(-5.0, 300.0)

plt.savefig(OUTPUT_FILE)

data_count = 0
for d in dataToPlot:
    data_count = data_count + len(d)
log("#data_points: " + str(data_count))

output_log.close()

