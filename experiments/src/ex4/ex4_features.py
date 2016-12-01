from data.data import loadData
from crossvalidation import findOutKForValidation
from crossvalidation import splitDataForXValidation
from models.model_randomforest import trainRandomForest, applyRandomForest
from error import maeDistribution
from graph import doGraph
from eval.mae import maeEval
from error import maeDistribution2
from graph import doGraph2
from error import reDistribution
from graph import doGraph3
from error import reDistribution2
from graph import doGraph4

DATA_DIRECTORY = "/media/sf_lur/data/"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex4/"

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

overall1 = []
for i in range(0,50):
    overall1.append(0)
overall2 = []
for i in range(0,101):
    overall2.append(0)
overall3 = []
for i in range(0,300):
    overall3.append(0)
overall4 = []
for i in range(-300,300):
    overall4.append(0)

# load data
data = {}
columns = []
loadData(DATA_DIRECTORY + "data_hour_2013.csv", [], data, columns)

# reduce the columns
columns = ['windspeed', 'pressure', 'month', 'winddirection', 'temperature', 'day_of_week', 'race_day', 'humidity', 'hour', 'bank_holiday', 'location', 'target']

values = findOutKForValidation("location", data)

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
    eval1 = maeEval(testData["target"], predictionData)
    eval2 = maeDistribution(testData["target"], predictionData, 50)
    eval3 = maeDistribution2(testData["target"], predictionData, 50)
    eval4 = reDistribution(testData["target"], predictionData)
    eval5 = reDistribution2(testData["target"], predictionData)
#     doGraph(eval2[1], "No2 hourly AE (MAE: " + str(eval1[1]) + ") @ " + sName, "AE (ug/m3)", OUTPUT_DIRECTORY + "ae_" + sName + ".png")
#     doGraph2(50, eval3[1], "No2 hourly error (MAE: " + str(eval1[1]) + ") @ " + sName, "error (ug/m3)", OUTPUT_DIRECTORY + "e_" + sName + ".png")
#     doGraph3(eval4[1], "No2 hourly RAE @ " + sName, "absolute relative error", OUTPUT_DIRECTORY + "rae_" + sName + ".png")
#     doGraph4(eval5[1], "No2 hourly RE @ " + sName, "relative error", OUTPUT_DIRECTORY + "re_" + sName + ".png")
    
    for i in range(0, len(eval2[1])):
        overall1[i] = overall1[i] + eval2[1][i]
    for i in range(0, len(eval3[1])):
        overall2[i] = overall2[i] + eval3[1][i]
    for i in range(0, len(eval4[1])):
        overall3[i] = overall3[i] + eval4[1][i]
    for i in range(0, len(eval5[1])):
        overall4[i] = overall4[i] + eval5[1][i]

doGraph(overall1, "No2 hourly AE", "AE (ug/m3)", OUTPUT_DIRECTORY + "feature_ae.png")
doGraph2(50, overall2, "No2 hourly error", "error (ug/m3)", OUTPUT_DIRECTORY + "feature_e.png")
doGraph3(overall3, "No2 hourly ARE", "absolute relative error", OUTPUT_DIRECTORY + "feature_rae.png")
doGraph4(overall4, "No2 hourly RE", "relative error", OUTPUT_DIRECTORY + "feature_re.png")
    
