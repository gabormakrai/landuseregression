from ex23_lib import loadEx23Data, doLineChart

DATA_FILE = "/experiments/ex23/file.csv"
WORK_DIRECTORY = "/experiments/ex23/"

stations, data = loadEx23Data(DATA_FILE)

print(str(stations))

dataToPlot = []
for station in stations:
    stationData = []
    for s in stations:
        stationData.append(data[station][s])
    dataToPlot.append(stationData)

doLineChart(
    WORK_DIRECTORY + "ex23_1.png", 
    "Prediction accuracy of models trained on 1 station data", 
    "Test Station", 
    "RMSE (ug/m3)", 
    dataToPlot, 
    stations)
