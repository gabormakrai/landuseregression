from data.data import loadData
from crossvalidation import findOutKForValidation, splitDataForXValidation
from models.model_linearregression import trainLinearRegression,\
    applyLinearRegression
from copy import deepcopy
from models.model_decisiontree import trainDecisionTree, applyDecisionTree
from graph import doBarChart
from ex2_library import hourCategory, raeEvaluation, hourCategoryOrder,\
    hourPostProcessResult
from models.model_randomforest import trainRandomForest, applyRandomForest
from models.model_nearestneighbors import trainNearestNeighbors,\
    applyNearestNeighbors
from models.model_svm import trainSVM, applySVM
from ex2_library import windspeedCategory, windspeedCategoryOrder,\
    windspeedPostProcessResult
from ex2_library import rmseEvaluation

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
DATA2_FILE = "/media/sf_lur/data/" + "data2_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex2/"

# load data
data1 = {}
columns1 = []
loadData(DATA_FILE, ["timestamp"], data1, columns1)
locationValues = findOutKForValidation("location", data1)

# load data2
data2 = {}
columns2 = []
loadData(DATA2_FILE, ["timestamp"], data2, columns2)
data2["hour"] = data1["hour"]

models = []

trainColumns1 = deepcopy(columns1)
trainColumns1.remove("location")
trainColumns2 = deepcopy(columns2)
trainColumns2.remove("location")

linearColumns1 = deepcopy(trainColumns1)
linearColumns1.remove("landuse_area")
linearColumns1.remove("leisure_area")

linearColumns2 = deepcopy(trainColumns2)
linearColumns2.remove("landuse_area")
linearColumns2.remove("leisure_area")

models.append({"name": "linear", "train": trainLinearRegression, "apply": applyLinearRegression, "data": deepcopy(data1), "columns": deepcopy(linearColumns1), "parameters": {'intercept': True, 'normalize': True, "features": columns1}})
models.append({"name": "lineardummy", "train": trainLinearRegression, "apply": applyLinearRegression, "data": deepcopy(data2), "columns": deepcopy(linearColumns2), "parameters": {'intercept': True, 'normalize': True, "features": columns2}})
models.append({"name": "nnr", "train": trainNearestNeighbors, "apply": applyNearestNeighbors, "data": deepcopy(data1), "columns": deepcopy(trainColumns1), "parameters": {'neighbors': 3, 'weights': 'distance', 'p': 1}})
models.append({"name": "svr", "train": trainSVM, "apply": applySVM, "data": deepcopy(data2), "columns": deepcopy(trainColumns2), "parameters": {'C': 1000, 'max_samples': 5000, 'n_estimators': 13}})
#models.append({"name": "ann", "train": trainNeuralNetwork, "apply": applyNeuralNetwork, "data": deepcopy(data2), "columns": deepcopy(trainColumns2), "parameters": {'hidden_neurons': 80, 'hidden_layers': 3, 'hidden_type': 'Linear', 'iteration': 1000}})
models.append({"name": "dtr", "train": trainDecisionTree, "apply": applyDecisionTree, "data": deepcopy(data1), "columns": deepcopy(trainColumns1), "parameters": {'leaf': 10}})
models.append({"name": "rfr", "train": trainRandomForest, "apply": applyRandomForest, "data": deepcopy(data1), "columns": deepcopy(trainColumns1), "parameters": {'estimators': 59, 'leaf': 9}})

def generateResult(model, getCategory, evalCategory, editCategoryOrder, postProcessResult):
    
    modelResult = {}
    
    print("Model " + model["name"] + "...")
    for location in locationValues:
        predictionCategory = {}
        testCategory = {}
        sName = stationNames[str(location)]
        print("  location: " + str(location) + " -> " + sName)
        trainData, testData = splitDataForXValidation(location, "location", model["data"])
        trainedModel = model["train"](trainData, model["columns"], "target", model["parameters"])
        predictionData = model["apply"](testData, trainedModel, 0)
        for i in range(0, len(predictionData)):
            category = getCategory(testData, i)
            if category not in predictionCategory:
                predictionCategory[category] = []
                testCategory[category] = []
            predictionCategory[category].append(predictionData[i])
            testCategory[category].append(testData["target"][i])
        
        for category in predictionCategory:
            result = evalCategory(testCategory[category], predictionCategory[category])
            if category not in modelResult:
                modelResult[category] = []
            modelResult[category].append(result)
    
    toPrintCategories = editCategoryOrder(modelResult)
    
    modelResult2 = postProcessResult(modelResult)
    
    for category in toPrintCategories:
        print("  " + str(category) + " -> " + str(modelResult2[category]))
        
    return modelResult2
        
for model in models:
    
    modelResult = generateResult(model, hourCategory, raeEvaluation, hourCategoryOrder, hourPostProcessResult)
    toPrintCategories = hourCategoryOrder(modelResult)
    values = []
    names = []
    for category in toPrintCategories:
        names.append(str(int(float(category))))
        values.append(modelResult[category])  
    doBarChart(OUTPUT_DIRECTORY + "hour_" + str(model["name"]) + "_rae.png", "Relative Absolute Error by hour (" + model["name"] + ")", "Hour of the day", "RAE", names, values)
    
    modelResult = generateResult(model, hourCategory, rmseEvaluation, hourCategoryOrder, hourPostProcessResult)
    toPrintCategories = hourCategoryOrder(modelResult)
    values = []
    names = []
    for category in toPrintCategories:
        names.append(str(int(float(category))))
        values.append(modelResult[category])  
    doBarChart(OUTPUT_DIRECTORY + "hour_" + str(model["name"]) + "_rmse.png", "RMSE by hour (" + model["name"] + ")", "Hour of the day", "RMSE", names, values)
    
    modelResult = generateResult(model, windspeedCategory, raeEvaluation, windspeedCategoryOrder, windspeedPostProcessResult)
    toPrintCategories = windspeedCategoryOrder(modelResult)
    values = []
    names = []
    for i in range(0, len(toPrintCategories)):
        category = toPrintCategories[i]
        names.append("<" + str((i+1)*3) + "m/s")
        values.append(modelResult[category]) 
    names[len(names) - 1] = "other"
    doBarChart(OUTPUT_DIRECTORY + "windspeed_" + str(model["name"]) + "_rae.png", "Relative Absolute Error by windspeed (" + model["name"] + ")", "Windspeed categories", "RAE", names, values)
    
    modelResult = generateResult(model, windspeedCategory, rmseEvaluation, windspeedCategoryOrder, windspeedPostProcessResult)
    toPrintCategories = windspeedCategoryOrder(modelResult)
    values = []
    names = []
    for i in range(0, len(toPrintCategories)):
        category = toPrintCategories[i]
        names.append("<" + str((i+1)*3) + "m/s")
        values.append(modelResult[category]) 
    names[len(names) - 1] = "other"
    doBarChart(OUTPUT_DIRECTORY + "windspeed_" + str(model["name"]) + "_rmse.png", "RMSE by windspeed (" + model["name"] + ")", "Windspeed categories", "RMSE", names, values)
    
