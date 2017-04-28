"""
Main modelling file
"""
import random
from data.data import loadData
from crossvalidation import crossValidation, crossValidationLocation
from eval.rmse import rmseEval
from norm import NONORMALIZATION, NORMALIZATION
from eval.correlation import correlationEval
from eval.mae import maeEval
from eval.fb import fbEval
from graph.graph import doErrorBar, doScatterDiagram, doHourlyErrorBar
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
from copy import copy, deepcopy

#OUTPUT_FILE = "/media/sf_lur/model_output/eval/lur2.csv"
#output = open(OUTPUT_FILE, 'w')
#output.write("method,eval,result\n")

years = [2012, 2013, 2014, 2015]
#years = [2012]

for year in years:

    # parameters
    dataFile1 = "/media/sf_lur/data/data_hour_" + str(year) + ".csv"
    dataFile2 = "/media/sf_lur/data/data2_hour_" + str(year) + ".csv"
    outputDir = "/media/sf_lur/model_output/eval/"
    
    # load the data, both of them
    data1 = {}
    columns1 = []
    loadData(dataFile1, ["timestamp"], data1, columns1)
    
    data2 = {}
    columns2 = []
    loadData(dataFile2, ["timestamp"], data2, columns2)
    
    random.seed(42)
    models = []
    
    linearColumns = deepcopy(columns1)
    linearColumns.remove("landuse_area")
    linearColumns.remove("leisure_area")
    linearColumns2 = deepcopy(columns2)
    linearColumns2.remove("landuse_area")
    linearColumns2.remove("leisure_area")
    linearColumns3 = deepcopy(columns1)
    linearColumns3.remove("landuse_area")
    linearColumns3.remove("leisure_area")
    for c in ['hour','day_of_week','month','bank_holiday','race_day']:
        linearColumns3.remove(c)
    for c in ['winddirection','windspeed','temperature','humidity','rain','pressure']:
        linearColumns3.remove(c)
        
#    models.append({"name": "linear_std", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": deepcopy(data1), "columns": linearColumns3, "parameters": {'intercept': True, 'normalize': True, "features": linearColumns3}})
    models.append({"name": "linear", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": deepcopy(data1), "columns": linearColumns, "parameters": {'intercept': True, 'normalize': True, "features": linearColumns}})
#    models.append({"name": "linear_dummy", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": deepcopy(data2), "columns": linearColumns2, "parameters": {'intercept': True, 'normalize': True, "features": linearColumns2}})
#     models.append({"name": "nnr", "norm": NONORMALIZATION, "train": trainNearestNeighbors, "apply": applyNearestNeighbors, "data": deepcopy(data1), "columns": deepcopy(columns1), "parameters": {'neighbors': 3, 'weights': 'distance', 'p': 1}})
#     models.append({"name": "svr", "norm": NONORMALIZATION, "train": trainSVM, "apply": applySVM, "data": deepcopy(data2), "columns": deepcopy(columns2), "parameters": {'C': 1000, 'max_samples': 5000, 'n_estimators': 13}})
#     models.append({"name": "ann", "norm": NORMALIZATION, "train": trainNeuralNetwork, "apply": applyNeuralNetwork, "data": deepcopy(data2), "columns": deepcopy(columns2), "parameters": {'hidden_neurons': 80, 'hidden_layers': 3, 'hidden_type': 'Linear', 'iteration': 1000}})
#     models.append({"name": "dtr", "norm": NONORMALIZATION, "train": trainDecisionTree, "apply": applyDecisionTree, "data": deepcopy(data1), "columns": deepcopy(columns1), "parameters": {'leaf': 10}})
#     models.append({"name": "rfr", "norm": NONORMALIZATION, "train": trainRandomForest, "apply": applyRandomForest, "data": deepcopy(data1), "columns": deepcopy(columns1), "parameters": {'estimators': 59, 'leaf': 9}})
    
    evalFunctions = [rmseEval, maeEval, correlationEval]
    evalFunctionNames = ['rmse', 'mae', 'r']
    
    # evalFunctions = [rmseEval, correlationEval, maeEval, nmseEval]
    # evalFunctionNames = ['rmse', 'r', 'mae', 'nmse']
    
    # evalFunctions = [rmseEval, correlationEval, rsquaredEval, maeEval, nmseEval, fbEval]
    # evalFunctionNames = ['rmse', 'r', 'r2', 'mae', 'nmse', 'fb']
    
    # results
    results = []
    
    # run cross validation for all the methods
    for model in models:
        random.seed(42)
        print("Running location based X-Validation with " + model["name"] + "(norm:" + str(model["norm"]) + ")")
        result = crossValidationLocation(model["data"], model["columns"], "target", model["norm"], model["train"], model["apply"], evalFunctions, model["parameters"])
        results.append([model["name"], result])
#         for ev in result["eval"]:
#             print("\t" + str(ev) + ": " + str(result["eval"][ev]))
#             for v in result["eval"][ev]:
#                 output.write(model["name"] + "," + str(ev) + "," + str(v) + "\n")

# output.close()
    
# #print out results    
# for result in results:
#     print(str(result[0]))
#     print(str(result[1]["avg"]))
#     print(str(result[1]["std"]))
#     print(str(result[1]["eval"]))
# 
# # create graphs
# for evalName in evalFunctionNames:
#      
#     names = []
#     means = []
#     stddevs = []
#      
#     xAxis = "Model name"
#      
#     if evalName == 'rmse':
#         yAxis = "RMSE (ug/m3)"
#     elif evalName == 'r':
#         yAxis = "Correlation - r"
#     elif evalName == 'r2':
#         yAxis = "Coefficient of determination - r2"
#     elif evalName == 'mae':
#         yAxis = "MAE (ug/m3)"
#     elif evalName == 'nmse':
#         yAxis = "NMSE (ug/m3)"
#     elif evalName == 'fb':
#         yAxis = "FB"
#                  
#     title = "Cross validation result"
#      
#     for result in results:
#         names.append(result[0])
#         means.append(result[1]['avg'][evalName])
#         stddevs.append(result[1]['std'][evalName])
#          
#     doErrorBar(outputDir + evalName + ".png", title, xAxis, yAxis, names, means, stddevs)
#
  
    for result in results:
        x = result[1]["scatter"]["test"]
        y = result[1]["scatter"]["prediction"]
        doScatterDiagram(outputDir + "scatter2_" + str(year) + ".png", "Model output (" + str(year) + ") - " + result[0], "Observation (ug/m3)", "Prediction (ug/m3)", x, y) 

