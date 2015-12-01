"""
Code to find out the best features and best parameters for linear_model.LinearRegression() algo 
"""
from data import loadData
from eval.rmse import rmseEval
from crossvalidation import crossValidation
from norm import NONORMALIZATION
from models.model_linearregression import trainLinearRegression,\
    applyLinearRegression
import random
import sys

# parameters

k = 8

featureSelectionIterationLimit = int(sys.argv[2])

parametersList = [
    {"normalize": False, "intercept": False},
    {"normalize": False, "intercept": True},
    {"normalize": True, "intercept": False},
    {"normalize": True, "intercept": True},
]

evalFunctions = [rmseEval]

print("Load data from " + sys.argv[1])

# load the data
data1 = {}
columns1 = []
# fixed file name:
# "f:\\transfer\\data\\data2.csv"
loadData(sys.argv[1], ["location", "timestamp"], data1, columns1)

def findBestFeautres(parameters, data, columns, targetColumn):
    
    bestFeatures = []
    
    for column in columns:
        if column != targetColumn:
            bestFeatures.append(column)
            
    for iteration in range(0, featureSelectionIterationLimit):
        
        # create the possible steps considering the current bestFeatures
        # possible step -> removing one feature
        
        print("iteration: " + str(iteration))
    
        possibleFeatures = []
        for skippedFeature in bestFeatures:
            features = []
            for feature in bestFeatures:
                if feature != skippedFeature:
                    features.append(feature)
            possibleFeatures.append(features)
            
        bestRMSE = 1000000.0
        bestRMSEFeatures = []
        
        for features in possibleFeatures:
            params = {}
            for p in parameters:
                params[p] = parameters[p]
            params["features"] = features
            random.seed(42)
            result = crossValidation(k, data, columns, targetColumn, NONORMALIZATION, trainLinearRegression, applyLinearRegression, evalFunctions, params)
            if result["avg"]["rmse"] < bestRMSE:
                bestRMSE = result["avg"]["rmse"]
                bestRMSEFeatures = features 
            print("current: " + str(result["avg"]["rmse"]) + ", best: " + str(bestRMSE))
        
        bestFeatures = bestRMSEFeatures
        print("rmse: " + str(bestRMSE) + ", features: " + str(features))
        
# find best features
print("Fixed parameters: " + str(parametersList[int(sys.argv[3])]))

findBestFeautres(parametersList[int(sys.argv[3])], data1, columns1, "nox")


