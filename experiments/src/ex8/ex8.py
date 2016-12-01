from ex8_lib import generateTimestampWeek
from ospm_data import loadOSPMData
from data.data import loadData
from ex8_ospm import ospm
from ex8_rf import rf

OSPM_DATA_DIRECTORY = "/media/sf_ospm/output/"
DATA_DIRECTORY = "/media/sf_lur/data/" 

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

print("Generate week categories for timestamps")
timestampWeekCategory = generateTimestampWeek() 
print("Done...")

print("Load ospm 2013 data")
ospmData2013 = {}
for stationName in stationNames:
    station = stationNames[stationName]
    loadOSPMData(OSPM_DATA_DIRECTORY + station + "_2013.dat", ospmData2013, station, "\t")
print("DOne...")

print("Load ospm 2014 data")
ospmData2014 = {}
for stationName in stationNames:
    station = stationNames[stationName]
    loadOSPMData(OSPM_DATA_DIRECTORY + station + "_2014.dat", ospmData2014, station, "\t")
print("DOne...")

print("Load data 2013...")
data2013 = {}
columns2013 = []
loadData(DATA_DIRECTORY + "data_hour_2013.csv", [], data2013, columns2013)
print("Done...")

print("Load data 2014...")
data2014 = {}
columns2014 = []
loadData(DATA_DIRECTORY + "data_hour_2014.csv", [], data2014, columns2014)
print("Done...")

for i in range(1, 53):
    week = 52 - i
    resOspm = ospm(week, timestampWeekCategory, stationNames, ospmData2013, ospmData2014, data2013, data2014)
    resRf = rf(week, timestampWeekCategory, stationNames, ospmData2013, ospmData2014, data2013, data2014)
    print(str(i) + "," + str(resOspm[1]) + "," + str(resRf[1]))


