from collections import defaultdict
import matplotlib.pyplot as plt
from data.data import loadData

DATA_FILE = "/data/london3_hour_2016.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_2.png"
OUTPUT_LOG_FILE = "/experiments/ex29/ex29_2.txt"

all_stations = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']
station_groups = [i % 5 for i in range(0, len(all_stations))]

output_log = open(OUTPUT_LOG_FILE, "w")

def log(line):
    output_log.write(line)
    output_log.write("\n")
    output_log.flush()
    print(line)

station_to_group = {}

groups = defaultdict(list)
for i in range(0, len(all_stations)):
    groups[station_groups[i]].append(all_stations[i])
    station_to_group[all_stations[i]] = station_groups[i] 

for i in range(0, len(groups)):
    log(str(groups[i]))

all_station2 = []
for i in range(0, 5):
    for s in groups[i]:
        all_station2.append(s)
log(str(all_station2))

# load the data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

log("all_features: " + str(columns))

# get the observation data for each station

stationData = defaultdict(list)
for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    value = data["target"][i]
    stationData[location].append(value)

fig = plt.figure(figsize=(9.36*1.7, 5.76*1.3))
ax = fig.add_subplot(111)

stationNames = []

dataToPlot = []
for s in all_station2:
    stationNames.append(s + " (" + str(len(stationData[s])) + ")\nGroup " + str(station_to_group[s] + 1))
    dataToPlot.append(stationData[s])

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(stationNames, rotation='vertical')

plt.ylabel("Concentration levels (ug/m3)")
plt.ylim(-5.0, 300.0)

fig.subplots_adjust(right=0.97, left=0.06, bottom=0.15, top=0.95)

plt.savefig(OUTPUT_FILE)

data_count = 0
for d in dataToPlot:
    data_count = data_count + len(d)
log("#data_points: " + str(data_count))

for i in range(0, 5):
    counter = 0
    for s in groups[i]:
        counter = counter + len(stationData[s])
    log("Group: " + str(i+1) + ": " + str(counter))

output_log.close()
