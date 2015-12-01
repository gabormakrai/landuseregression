from eval.rmse import rmseEval
from data import loadData
from norm import NONORMALIZATION
from models.model_decisiontree import trainDecisionTree, applyDecisionTree
from crossvalidation import crossValidation
import random

# parameters

k = 8

parametersList = []

for i in range(3, 40):
    parametersList.append({"depth": i})

for i in range(1, 25):
    parametersList.append({"leaf": i})

evalFunctions = [rmseEval]

# load the data
data1 = {}
columns1 = []
loadData("f:\\transfer\\data\\data.csv", ["location", "timestamp"], data1, columns1)

for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data1, columns1, "nox", NONORMALIZATION, trainDecisionTree, applyDecisionTree, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))
    
# load the data
data2 = {}
columns2 = []
loadData("f:\\transfer\\data\\data2.csv", ["location", "timestamp"], data2, columns2)

for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data2, columns2, "nox", NONORMALIZATION, trainDecisionTree, applyDecisionTree, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))
