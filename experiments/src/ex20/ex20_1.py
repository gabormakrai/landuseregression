import matplotlib.pyplot as plt
from airquality import loadFile

DATA_DIRECTORY = "/media/sf_lur/data/aq/"
OUTPUT_FILE = "/media/sf_lur/experiments/ex20/fig1.png"

stations = ["Fishergate", "Fulford", "Gillygate", "Heworth", "Lawrence"]
years = [2013]

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

# stations.append("All")
# 
# allData = []
# for values in dataToPlot:
#     for v in values:
#         allData.append(v)
#         
# dataToPlot.append(allData)

fig = plt.figure(None, figsize=(6, 6))
ax = fig.add_subplot(111)

print(str(len(dataToPlot)))
print(str(len(stations)))

stations = ["Fishergate\n(8496 records)", "Fulford\n(8228 records)", "Gillygate\n(6799 records)", "Heworth\n(7600 records)", "Lawrence\n(7858 records)"]

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(stations, rotation='vertical')

plt.ylabel("Concentration levels (ug/m3)")
plt.ylim(-5.0, 100.0)

fig.subplots_adjust(bottom=0.3)

plt.savefig(OUTPUT_FILE)


