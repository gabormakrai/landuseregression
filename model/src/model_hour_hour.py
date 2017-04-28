"""
Main modelling file
"""
import random
from data import loadData
from crossvalidation import crossValidation, crossValidationHour,\
    crossValidationLocationHour
from eval.rmse import rmseEval
from norm import NONORMALIZATION, NORMALIZATION
from eval.correlation import correlationEval
from eval.mae import maeEval
from eval.fb import fbEval
from graph import doErrorBar, doScatterDiagram, doHourlyErrorBar
from models.model_linearregression import trainLinearRegression,\
    applyLinearRegression
from models.model_nearestneighbors import trainNearestNeighbors,\
    applyNearestNeighbors
from models.model_decisiontree import trainDecisionTree, applyDecisionTree
from models.model_randomforest import trainRandomForest, applyRandomForest
from models.model_ann import trainNeuralNetwork, applyNeuralNetwork
from models.model_svm import trainSVM, applySVM
from eval.rsquared import rsquaredEval
from eval.nmse import nmseEval
from models.model_avg import trainAverage, applyAverage
from copy import deepcopy

# parameters
k = 8
dataFile1 = "/media/sf_lur/data/data_hour.csv"
#dataFile2 = "/media/sf_Google_Drive/transfer/data/data2.csv"
outputDir = "/media/sf_lur/model_output/"

# load the data, both of them
data1 = {}
columns1 = []
loadData(dataFile1, ["timestamp", "landuse_area"], data1, columns1)

# data2 = {}
# columns2 = []
# loadData(dataFile2, ["location", "timestamp"], data2, columns2)

random.seed(42)
models = []
models.append({"name": "linear", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": deepcopy(data1), "columns": deepcopy(columns1), "parameters": {'intercept': True, 'normalize': True, "features": columns1}})
#models.append({"name": "linear_dummy", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": data2, "columns": columns2, "parameters": {'intercept': True, 'normalize': True, "features": columns2}})
#models.append({"name": "nnr", "norm": NONORMALIZATION, "train": trainNearestNeighbors, "apply": applyNearestNeighbors, "data": data1, "columns": columns1, "parameters": {'neighbors': 3, 'weights': 'distance', 'p': 1}})
#models.append({"name": "svr", "norm": NONORMALIZATION, "train": trainSVM, "apply": applySVM, "data": data2, "columns": columns2, "parameters": {'C': 1000, 'max_samples': 5000, 'n_estimators': 13}})
#models.append({"name": "ann", "norm": NORMALIZATION, "train": trainNeuralNetwork, "apply": applyNeuralNetwork, "data": data2, "columns": columns2, "parameters": {'hidden_neurons': 80, 'hidden_layers': 3, 'hidden_type': 'Linear', 'iteration': 1000}})
models.append({"name": "dtr", "norm": NONORMALIZATION, "train": trainDecisionTree, "apply": applyDecisionTree, "data": deepcopy(data1), "columns": deepcopy(columns1), "parameters": {'leaf': 10}})
models.append({"name": "rfr", "norm": NONORMALIZATION, "train": trainRandomForest, "apply": applyRandomForest, "data": deepcopy(data1), "columns": deepcopy(columns1), "parameters": {'estimators': 59, 'leaf': 9}})
# models.append({"name": "avg", "norm": NONORMALIZATION, "train": trainAverage, "apply": applyAverage, "data": data1, "columns": columns1, "parameters": {}})

evalFunctions = [rmseEval, correlationEval, rsquaredEval, maeEval, nmseEval, fbEval]
evalFunctionNames = ['rmse', 'r', 'r2', 'mae', 'nmse', 'fb']

# results
results = {}

# run cross validation for all the methods
for model in models:
    print("Running location based X-Validation with " + model["name"] + "(norm:" + str(model["norm"]) + ")")
    result = crossValidationLocationHour(model["data"], model["columns"], "target", model["norm"], model["train"], model["apply"], evalFunctions, model["parameters"])
    results[model["name"]] = result

for evalName in evalFunctionNames:
    
    barData = {}
    
    for modelName in results:
        result = results[modelName]
        modelData = []
        for hour in range(0,24):
            modelData.append(result[evalName][hour]) 
        barData[modelName] = modelData
    
    xAxis = "Hour"
 
    if evalName == 'rmse':
        yAxis = "RMSE (ug/m3)"
    elif evalName == 'r':
        yAxis = "Correlation - r"
    elif evalName == 'r2':
        yAxis = "Coefficient of determination - r2"
    elif evalName == 'mae':
        yAxis = "MAE (ug/m3)"
    elif evalName == 'nmse':
        yAxis = "NMSE (ug/m3)"
    elif evalName == 'fb':
        yAxis = "FB"        
         
    title = "Cross validation result (hour)"

    colors = {}
    colorIndex = 0
    for modelName in results:
        c = 'r'
        if colorIndex == 1:
            c = 'g'
        elif colorIndex == 2:
            c = 'b'
        elif colorIndex == 3:
            c = 'y'
        elif colorIndex == 4:
            c = 'm'
        elif colorIndex == 5:
            c = 'c'
        colors[modelName] = c
        colorIndex = colorIndex + 1
    
    modelNames = []
    for model in models:
        modelNames.append(model["name"])
    
    doHourlyErrorBar(outputDir + "hour_" + evalName + ".png", title, xAxis, yAxis, modelNames, barData, colors)
