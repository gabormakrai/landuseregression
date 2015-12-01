"""
Main modelling file
"""
import random
from data import loadData
from crossvalidation import crossValidation
from eval.rmse import rmseEval
from norm import NONORMALIZATION
from eval.correlation import correlationEval
from eval.mae import maeEval
from eval.fb import fbEval
from graph import doErrorBar, doScatterDiagram
from models.model_linearregression import trainLinearRegression,\
    applyLinearRegression
from models.model_nearestneighbors import trainNearestNeighbors,\
    applyNearestNeighbors
from models.model_decisiontree import trainDecisionTree, applyDecisionTree
from models.model_randomforest import trainRandomForest, applyRandomForest

# parameters
k = 8
dataFile1 = "f:\\transfer\\data\\data.csv"
dataFile2 = "f:\\transfer\\data\\data2.csv"
outputDir = "f:\\transfer\\model_output\\"

# load the data, both of them
data1 = {}
columns1 = []
loadData(dataFile1, ["location", "timestamp"], data1, columns1)

data2 = {}
columns2 = []
loadData(dataFile2, ["location", "timestamp"], data2, columns2)

random.seed(42)
models = []
models.append({"name": "linear", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": data1, "columns": columns1, "parameters": {'intercept': True, 'normalize': True, "features": columns1}})
models.append({"name": "linear_dummy", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": data2, "columns": columns2, "parameters": {'intercept': True, 'normalize': True, "features": columns2}})
models.append({"name": "nnr_k_3_p_1", "norm": NONORMALIZATION, "train": trainNearestNeighbors, "apply": applyNearestNeighbors, "data": data1, "columns": columns1, "parameters": {'neighbors': 3, 'weights': 'distance', 'p': 1}})
models.append({"name": "dtr_leaf_10", "norm": NONORMALIZATION, "train": trainDecisionTree, "apply": applyDecisionTree, "data": data1, "columns": columns1, "parameters": {'leaf': 10}})
models.append({"name": "dtr_depth_13", "norm": NONORMALIZATION, "train": trainDecisionTree, "apply": applyDecisionTree, "data": data1, "columns": columns1, "parameters": {'depth': 13}})
models.append({"name": "rfr_est_49_depth_14", "norm": NONORMALIZATION, "train": trainRandomForest, "apply": applyRandomForest, "data": data1, "columns": columns1, "parameters": {'depth': 14, 'estimators': 49}})

evalFunctions = [rmseEval, correlationEval, maeEval, fbEval]
evalFunctionNames = ['rmse', 'r']

# results
results = []

# run cross validation for all the methods
for model in models:
    print("Running " + str(k) + "-fold X-Validation with " + model["name"] + "(norm:" + str(model["norm"]) + ")")
    result = crossValidation(k, model["data"], model["columns"], "nox", model["norm"], model["train"], model["apply"], evalFunctions, model["parameters"])
    results.append([model["name"], result])

#print out results    
for result in results:
    print(str(result[0]) + str(result[1]["avg"]))

# create graphs
for evalName in evalFunctionNames:
    
    names = []
    means = []
    stddevs = []
    
    xAxis = "Model name"
    
    if evalName == 'rmse':
        yAxis = "RMSE (ug/m3)"
    elif evalName == 'r':
        yAxis = "Correlation - r"
        
    title = "Cross validation result"
    
    for result in results:
        names.append(result[0])
        means.append(result[1]['avg'][evalName])
        stddevs.append(result[1]['std'][evalName])
        
    doErrorBar(outputDir + evalName + ".png", title, xAxis, yAxis, names, means, stddevs)

for result in results:
    x = result[1]["scatter"]["test"]
    y = result[1]["scatter"]["prediction"]
    doScatterDiagram(outputDir + "scatter_" + result[0] + ".png", "Model output", "observation", "prediction", x, y) 
