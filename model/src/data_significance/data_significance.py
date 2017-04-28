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

outputFile = "/media/sf_lur/data_significance/result_lin.csv"

years = [2012, 2013, 2014, 2015]

dataFiles = {}
for year in years:
    dataFiles[year] = "/media/sf_lur/data/data_hour_" + str(year) + ".csv"

evalFunction = rmseEval
evalFunctionName = 'rmse'

output = open(outputFile, 'w')
output.write("group," + evalFunctionName + "\n")

def doEval(landuse, topo, traffic_static, traffic_dynamic, weather, time, output):
    
    if landuse == False and topo == False and traffic_dynamic == False and traffic_static == False and weather == False and time == False:
        return
    
    groupName = "lu"
    if landuse == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "to"
    if topo == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
    
    groupName = groupName + "ts"
    if traffic_static == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "td"
    if traffic_dynamic == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "we"
    if weather == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "ti"
    if time == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    print("Group: " + groupName)
        
    data = {}
    columns = {}
    
    columnsToSkip = ['timestamp']
    
    if landuse == False:
        columnsToSkip.append('leisure_area')
        columnsToSkip.append('landuse_area')
    if topo == False:
        columnsToSkip.append('buildings_number')
        columnsToSkip.append('buildings_area')
    if traffic_static == False:
        columnsToSkip.append('lane_length')
        columnsToSkip.append('length')
    if traffic_dynamic == False:
        columnsToSkip.append('traffic_length_car')
        columnsToSkip.append('traffic_length_lgv')
        columnsToSkip.append('traffic_length_hgv')
    if weather == False:
        columnsToSkip.append('winddirection')
        columnsToSkip.append('windspeed')
        columnsToSkip.append('temperature')
        columnsToSkip.append('rain')
        columnsToSkip.append('pressure')
    if time == False:
        columnsToSkip.append('hour')
        columnsToSkip.append('day_of_week')
        columnsToSkip.append('month')
        columnsToSkip.append('bank_holiday')
        columnsToSkip.append('race_day')

    for year in years:
        columns[year] = []
        data[year] = {}
        loadData(dataFiles[year], columnsToSkip, data[year], columns[year])            
    
    for year in years:
        print("year " + str(year))
        model = {"name": "linear", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": data[year], "columns": columns[year], "parameters": {'intercept': True, 'normalize': True, "features": columns[year]}}
        
#        model = {"name": "rfr", "norm": NONORMALIZATION, "train": trainRandomForest, "apply": applyRandomForest, "data": data[year], "columns": columns[year], "parameters": {'estimators': 50, 'leaf': 10}}
        result = crossValidationLocation(model["data"], model["columns"], "target", model["norm"], model["train"], model["apply"], [evalFunction], model["parameters"])
        print(str(result["eval"]))
        for value in result["eval"][evalFunctionName]:
            output.write(str(groupName) + "," + str(value) + "\n")
             
        

for landuse in [True, False]:
    for topo in [True, False]:
        for traffic_static in [True, False]:
            for traffic_dynamic in [True, False]:
                for weather in [True, False]:
                    for time in [True, False]:
                        doEval(landuse, topo, traffic_static, traffic_dynamic, weather, time, output)

#doEval(True, False, True, False, False, True, output)

output.close()
