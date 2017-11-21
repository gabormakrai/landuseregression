from collections import defaultdict
import matplotlib.pyplot as plt
from data.data import loadData

all_stations = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']
station_groups = [i % 5 for i in range(0, len(all_stations))]

station_to_group = {}

groups = defaultdict(list)
for i in range(0, len(all_stations)):
    groups[station_groups[i]].append(all_stations[i])
    station_to_group[all_stations[i]] = station_groups[i] 

for i in range(0, len(groups)):
    print(str(groups[i]))

all_station2 = []
for i in range(0, 5):
    for s in groups[i]:
        all_station2.append(s)
print(str(all_station2))

DATA_FILE1 = "/data/london3_hour_2016.csv"
OUTPUT_FILE1 = "/experiments/ex26/ex26_1.png"

# load the data
data = {}
columns = []
loadData(DATA_FILE1, [], data, columns)

# get the observation data for each station

stationData = defaultdict(list)
for i in range(0, len(data["target"])):
    location = str(data["location"][i])
    value = data["target"][i]
    stationData[location].append(value)

fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)

stationNames = []

dataToPlot = []
for s in all_station2:
    stationNames.append(s + " (" + str(len(stationData[s])) + ")\nGroup " + str(station_to_group[s] + 1))
    dataToPlot.append(stationData[s])

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(stationNames, rotation='vertical')

plt.title("Grouped data of " + str(len(stationNames)) + " stations (including ATC data)")

plt.ylabel("Concentration levels (ug/m3)")
plt.ylim(-5.0, 300.0)

plt.savefig(OUTPUT_FILE1)

data_count = 0
for d in dataToPlot:
    data_count = data_count + len(d)
print("#data_points: " + str(data_count))

for i in range(0, 5):
    counter = 0
    for s in groups[i]:
        counter = counter + len(stationData[s])
    print("Group: " + str(i+1) + ": " + str(counter))