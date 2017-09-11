from ex24_lib import loadEx24Data, doLineChart

DATA_FILE_TW = "/experiments/ex24/ex25_5_tw.csv"
DATA_FILE_TWA = "/experiments/ex24/ex25_5_twa.csv"
DATA_FILE_ALL = "/experiments/ex24/ex25_5_all.csv"

OUTPUT_FILE_TW = "/experiments/ex24/ex24_6_tw.png"
OUTPUT_FILE_TWA = "/experiments/ex24/ex24_6_twa.png"
OUTPUT_FILE_ALL = "/experiments/ex24/ex24_6_all.png"

def doOne(inputFile, outputFile):

    stations, data = loadEx24Data(inputFile)
    
    print(str(stations))
    
    dataToPlot = []
    for station in stations:
        stationData = []
        for s in stations:
            stationData.append(data[station][s])
        dataToPlot.append(stationData)
    
    doLineChart(
        outputFile, 
        "Prediction accuracy of models trained on 1 station data", 
        "Test Station", 
        "RMSE (ug/m3)", 
        dataToPlot, 
        stations)

doOne(DATA_FILE_TW, OUTPUT_FILE_TW)
doOne(DATA_FILE_TWA, OUTPUT_FILE_TWA)
doOne(DATA_FILE_ALL, OUTPUT_FILE_ALL)
