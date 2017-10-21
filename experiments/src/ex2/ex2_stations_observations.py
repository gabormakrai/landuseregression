import matplotlib.pyplot as plt
from collections import defaultdict
from data.data import loadData

DATA_FILE = "/data/york_hour_2013.csv"
OUTPUT_FILE = "/experiments/ex2/ex2_station_observations.png"

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

stations = [(2.0, "Fulford"), (4.0, "Heworth"), (8.0, "Fishergate"), (7.0, "Nunnery"), (3.0, "Gillygate"), (5.0, "Holgate"), (6.0, "Lawrence")]

dataPerStation = defaultdict(list)

for i in range(0, len(data["target"])):
    location = data["location"][i]
    clevel = data["target"][i]
    dataPerStation[location].append(clevel)

dataToPlot = []
names = []

for stuple in stations:
    d = dataPerStation[stuple[0]]
    dataToPlot.append(d)
    names.append(stuple[1] + "\n(" + str(len(d)) + " records)")

fig = plt.figure(None, figsize=(10, 4))
ax = fig.add_subplot(111)

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names) #, rotation='vertical')

plt.ylabel("Concentration levels (ug/m3)")
plt.ylim(-5.0, 100.0)

fig.subplots_adjust(bottom=0.3)

plt.savefig(OUTPUT_FILE)


