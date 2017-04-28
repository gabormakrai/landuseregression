from data.data import loadData
from errors import ae
from eval.rmse import rmseEval
from ex18_lib import plotArray
from sklearn.tree.tree import DecisionTreeClassifier
from crossvalidation import generateTrainingData
from sklearn.metrics.classification import accuracy_score, confusion_matrix

INPUT_DIRECTORY = "/media/sf_lur/experiments/ex18/" 
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex18/"

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

locations = [2.0, 3.0, 4.0, 8.0]
#locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

models = ["tw", "twa", "all"]

data = {}
columns = {}
for m in models:
    d = {}
    c = []
    loadData(INPUT_DIRECTORY + m + ".csv", [], d, c)
    data[m] = d
    columns[m] = c

errorsTimestamps = {}
eData = {}

for m in models:
    
    errors = {}
    for l in locations:
        errors[l] = 0
    
    errorsTimestamps[m] = set()  
    records = len(data[m]['target'])
    
    print("Overall:")
    
    print("\t" + "#records: " + str(records))
    rmse = rmseEval(data[m]['target'], data[m]['prediction'])[1]
    print("\t" + "rmse: " + str(rmse))
     
    absoluteError = ae(data[m]['target'], data[m]['prediction'])
    absoluteError.sort()
    
    eData[m] = absoluteError
        
    # error without records have ae > 20.0
    
    data2 = {}
    for c in columns[m]:
        data2[c] = []
    for i in range(0, records):
        if abs(data[m]['target'][i] - data[m]['prediction'][i]) < 20.0:
            for c in columns[m]:
                data2[c].append(data[m][c][i])
    
    records2 = len(data2['target'])
    
    print("Only records with abs_error < 20.0")
    
    print("\t" + "#records: " + str(records2))
    rmse = rmseEval(data2['target'], data2['prediction'])[1]
    print("\t" + "rmse: " + str(rmse))
    
    print("Records > 20.0")
    print("\t" + "#records: " + str(records - records2))
    
    for i in range(0, records):
        if abs(data[m]['target'][i] - data[m]['prediction'][i]) > 20.0:
            # counting them
            errors[data[m]["location"][i]] = errors[data[m]["location"][i]] + 1
            # generate hash for timestamp+location
            h = int(str(int(data[m]['timestamp'][i]))[4:])
            h = 1000000*int(data[m]["location"][i]) + h
            errorsTimestamps[m].add(h)  
    
    for l in locations:
        print(str(l) + " / " + stationNames[str(l)] + " -> " + str(errors[l]))    

plotArray(OUTPUT_DIRECTORY + "ae.png", "Absolute error plot", "Predictions", "Prediction error (ug/m3)", ["T+W", "T+W+A", "All"], [eData["tw"], eData["twa"], eData["all"]])


print("Errors timestamps overlap...")

print("TW and TWA")

counter = 0
for v in errorsTimestamps["tw"]:
    if v in errorsTimestamps["twa"]:
        counter = counter + 1

print("\t" + str(counter))

print("TW but not TWA")

counter = 0
for v in errorsTimestamps["tw"]:
    counter = counter + 1
    if v in errorsTimestamps["twa"]:
        counter = counter - 1

print("\t" + str(counter))

print("TWA but not TW")

counter = 0
for v in errorsTimestamps["twa"]:
    counter = counter + 1
    if v in errorsTimestamps["tw"]:
        counter = counter - 1

print("\t" + str(counter))

print("Best of each model... (TW and TWA)")

combinedPrediction = []
combinedPrediction2 = []

twBetter = 0
twaBetter = 0

records = len(data["tw"]["location"])
label = []

for i in range(0, records):
    aeTW = abs(data["tw"]["prediction"][i] - data["tw"]["target"][i])
    aeTWA = abs(data["twa"]["prediction"][i] - data["twa"]["target"][i])
    if aeTW < aeTWA:
        combinedPrediction.append(data["tw"]["prediction"][i])
        twBetter = twBetter + 1
        label.append(0)
    else:
        combinedPrediction.append(data["twa"]["prediction"][i])
        twaBetter = twaBetter + 1
        label.append(1)
    combinedPrediction2.append((data["tw"]["prediction"][i] + data["twa"]["prediction"][i]) / 2.0)

print("TW better:" + str(twBetter))
print("TWA better:" + str(twaBetter))

rmse = rmseEval(data["tw"]['target'], combinedPrediction)[1]
print("rmse: " + str(rmse))

rmse = rmseEval(data["tw"]['target'], combinedPrediction2)[1]
print("rmse: " + str(rmse))

print("identification test:")
  
identificationColumns = []
for c in columns["all"]:
    if c not in ['target', 'prediction', 'timestamp', 'location']:
        identificationColumns.append(c)
 
clf = DecisionTreeClassifier()
 
traintestX = generateTrainingData(data["all"], identificationColumns) 
 
clf = clf.fit(traintestX, label)
prediction = clf.predict(traintestX)
 
a = accuracy_score(label, prediction)
print(str(a))
 
a = accuracy_score(label, prediction, normalize=False)
print(str(a))
 
a = confusion_matrix(label, prediction)
print(str(a))
 
# with open(OUTPUT_DIRECTORY + "dt.dot", 'w') as f:
#     f = tree.export_graphviz(clf, out_file=f, feature_names=identificationColumns)#, max_depth=10)



