from data.data import loadData
from ex18_lib import doBoxplot

INPUT_DIRECTORY = "/experiments/ex18/"
OUTPUT_DIRECTORY = "/experiments/ex18/"  

dataTW = {}
columnsTW = []
loadData(INPUT_DIRECTORY + "tw.csv", [], dataTW, columnsTW)

dataTWA = {}
columnsTWA = []
loadData(INPUT_DIRECTORY + "twa.csv", [], dataTWA, columnsTWA)

dataWA = {}
columnsWA = []
loadData(INPUT_DIRECTORY + "wa.csv", [], dataWA, columnsWA)

names = []
data = []

names.append("e(T+W)")
d = []
for i in range(0, len(dataTW["prediction"])):
    ae = abs(dataTW["prediction"][i] - dataTW["target"][i])
    d.append(ae)
data.append(d)

names.append("e(T+W+A)")
d = []
for i in range(0, len(dataTW["prediction"])):
    ae = abs(dataTWA["prediction"][i] - dataTWA["target"][i])
    d.append(ae)
data.append(d)

names.append("e(W+A)")
d = []
for i in range(0, len(dataTW["prediction"])):
    ae = abs(dataWA["prediction"][i] - dataWA["target"][i])
    d.append(ae)
data.append(d)

names.append("e(TWA)-e(TW)")
d = []
for i in range(0, len(dataTW["prediction"])):
    aeTWA = abs(dataTWA["prediction"][i] - dataTWA["target"][i])
    aeTW = abs(dataTW["prediction"][i] - dataTW["target"][i])
    d.append(aeTWA-aeTW)
data.append(d)

names.append("e(WA)-e(TW)")
d = []
for i in range(0, len(dataTW["prediction"])):
    aeWA = abs(dataWA["prediction"][i] - dataWA["target"][i])
    aeTW = abs(dataTW["prediction"][i] - dataTW["target"][i])
    d.append(aeWA-aeTW)
data.append(d)

names.append("e(WA)-e(TWA)")
d = []
for i in range(0, len(dataTW["prediction"])):
    aeWA = abs(dataWA["prediction"][i] - dataWA["target"][i])
    aeTWA = abs(dataTWA["prediction"][i] - dataTWA["target"][i])
    d.append(aeWA-aeTWA)
data.append(d)

doBoxplot(OUTPUT_DIRECTORY + "ex18_error_boxplot.png", "Absolute error boxplot", "Absolute error (ug/m3)", True, data, names)
doBoxplot(OUTPUT_DIRECTORY + "ex18_error_boxplot2.png", "Absolute error boxplot", "Absolute error (ug/m3)", False, data, names)

print("check data...")

print("\tTW records:" + str(len(dataTW["prediction"])))
print("\tTWA records:" + str(len(dataTWA["prediction"])))
print("\tWA records:" + str(len(dataWA["prediction"])))

sum1 = 0.0
sum2 = 0.0
for i in range(0, len(dataTW["prediction"])):
    sum1 = sum1 + abs(dataTW["target"][i] - dataTWA["target"][i])
    sum2 = sum2 + abs(dataTW["target"][i] - dataWA["target"][i])    
    
print(str(sum1))
print(str(sum2))

# generate data

records = len(dataTW["prediction"])

aeTW1 = []
aeTW2 = []

aeTWA1 = []
aeTWA2 = []

aeWA1 = []
aeWA2 = []

for i in range(0, records):
    weekdays = dataTW["day_of_week"][i]
    holidays = dataTW["bank_holiday"][i]
    windspeed = dataTW["windspeed"][i]
    hour = dataTW["hour"][i]
    temperature = dataTW["temperature"][i]
    month = dataTW["month"][i]
    
    if (weekdays < 6 and holidays < 0.5 and hour > 3.5 and hour < 7.5 and windspeed < 3.0 and temperature < 8.0):
        aeTW1.append( abs(dataTW["prediction"][i] - dataTW["target"][i]) )
        aeTWA1.append( abs(dataTWA["prediction"][i] - dataTWA["target"][i]) )
        aeWA1.append( abs(dataWA["prediction"][i] - dataWA["target"][i]) )
        
    if (weekdays < 6 and holidays < 0.5 and hour > 15.5 and hour < 19.5 and windspeed < 3.0 and temperature < 8.0):
        aeTW2.append( abs(dataTW["prediction"][i] - dataTW["target"][i]) )
        aeTWA2.append( abs(dataTWA["prediction"][i] - dataTWA["target"][i]) )
        aeWA2.append( abs(dataWA["prediction"][i] - dataWA["target"][i]) )

names = []
names.append("TW\nmorning")
names.append("TWA\nmorning")
names.append("WA\nmorning")
names.append("TW\nafternoon")
names.append("TWA\nafternoon")
names.append("WA\nafternoon")

# names.append("TW morning (" + str(len(aeTW1)) + ")")
# names.append("TWA morning (" + str(len(aeTWA1)) + ")")
# names.append("WA morning (" + str(len(aeWA1)) + ")")
# names.append("TW aftern. peak (" + str(len(aeTW2)) + ")")
# names.append("TWA aftern. peak (" + str(len(aeTWA2)) + ")")
# names.append("WA aftern. peak (" + str(len(aeWA2)) + ")")

data = [aeTW1, aeTWA1, aeWA1, aeTW2, aeTWA2, aeWA2]

doBoxplot(OUTPUT_DIRECTORY + "ex18_error_boxplot3.png", "Absolute error boxplot", "Absolute error (ug/m3)", True, data, names)
doBoxplot(OUTPUT_DIRECTORY + "ex18_error_boxplot4.png", "Absolute error boxplot", "Absolute error (ug/m3)", False, data, names)
