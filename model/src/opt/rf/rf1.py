from eval.rmse import rmseEval
from data import loadData
from norm import NONORMALIZATION
from crossvalidation import crossValidation
import random
from models.model_randomforest import trainRandomForest, applyRandomForest

# parameters

k = 8

parametersList = []

for d in range(3, 25):
    for estimators in range(3, 70):
        parametersList.append({"depth": d, "estimators": estimators})

for l in range(2, 30):
    for estimators in range(3, 70):
        parametersList.append({"leaf": l, "estimators": estimators})

evalFunctions = [rmseEval]

# load the data
data1 = {}
columns1 = []
loadData("f:\\transfer\\data\\data.csv", ["location", "timestamp"], data1, columns1)

for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data1, columns1, "nox", NONORMALIZATION, trainRandomForest, applyRandomForest, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))
    
# load the data
data2 = {}
columns2 = []
loadData("f:\\transfer\\data\\data2.csv", ["location", "timestamp"], data2, columns2)
 
for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data2, columns2, "nox", NONORMALIZATION, trainRandomForest, applyRandomForest, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))
