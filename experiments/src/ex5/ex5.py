from data.data import loadData
from crossvalidation import findOutKForValidation
from crossvalidation import splitDataForXValidation
from models.model_randomforest import trainRandomForest, applyRandomForest
from error import raeEval
from copy import deepcopy

DATA_DIRECTORY = "/media/sf_lur/data/"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex5/"

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

# load data
data = {}
columns = []
loadData(DATA_DIRECTORY + "data_hour_2013.csv", ["timestamp"], data, columns)

values = findOutKForValidation("location", data)

output = open(OUTPUT_DIRECTORY + "errors_rae.csv", 'w')
outputColumns = []

for v in values:
    sName = stationNames[str(v)]
    print("location: " + str(v) + " -> " + sName)
    trainData, testData = splitDataForXValidation(v, "location", data)
    trainColumns = []
    for c in trainData:
        if c != "target":
            trainColumns.append(c)
    
    model = trainRandomForest(trainData, trainColumns, "target", {'estimators': 59, 'leaf': 9})
    predictionData = applyRandomForest(testData, model, 0)
    rae = raeEval(testData["target"], predictionData)
    print(str(len(rae[1])))
    print(str(len(predictionData)))
    print(str(len(testData["target"])))
    
    # write header
    if len(outputColumns) == 0:
        outputColumns = deepcopy(trainColumns)
        for c in outputColumns:
            output.write(c)
            output.write(",")
        output.write("error_rae\n")
    
    for i in range(0, len(testData["target"])):
        for c in outputColumns:
            output.write(str(testData[c][i]))
            output.write(",")
        output.write(str(rae[1][i]))
        output.write("\n")

output.close()
