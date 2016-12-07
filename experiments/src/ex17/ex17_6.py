import matplotlib.pyplot as plt
from airquality import loadFile

DATA_DIRECTORY = "/media/sf_lur/data/aq/"
OUTPUT_FILE = "/media/sf_lur/experiments/ex17/graph6.png"

stations = ["Fishergate", "Fulford", "Gillygate", "Heworth", "Holgate", "Lawrence", "Nunnery"]
years = [2012, 2013, 2014, 2015]

dataToPlot = []
for station in stations:
    dataToPlot.append([])

print("Loading data...")

for year in years:
    for i in range(0, len(stations)):
        station = stations[i]
        data = {}
        fileName = DATA_DIRECTORY + station + "_" + str(year) + ".csv"
        print("\tLoading data from " + fileName + "...")
        loadFile("no2", fileName, data)
        for timestampKey in data:
            dataToPlot[i].append(data[timestampKey])
        print("\tDone...")

print("Done...")

stations.append("All")

allData = []
for values in dataToPlot:
    for v in values:
        allData.append(v)
        
dataToPlot.append(allData)

fig = plt.figure(None, figsize=(10, 10))
ax = fig.add_subplot(111)

print(str(len(dataToPlot)))
print(str(len(stations)))

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(stations, rotation='vertical')

plt.ylabel("Concentration levels (ug/m3)")
plt.ylim(-5.0, 100.0)

plt.savefig(OUTPUT_FILE)


