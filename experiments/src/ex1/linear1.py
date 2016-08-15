"""
Code to find out the best features and best parameters for linear_model.LinearRegression() algo 
"""
from data.data import loadData
from eval.rmse import rmseEval
from crossvalidation import crossValidation
from norm import NONORMALIZATION
from models.model_linearregression import trainLinearRegression,\
    applyLinearRegression
import random

# parameters

k = 8

featureSelectionIterationLimit = int(10)

parametersList = [
    {"normalize": False, "intercept": False},
    {"normalize": False, "intercept": True},
    {"normalize": True, "intercept": False},
    {"normalize": True, "intercept": True},
]

evalFunctions = [rmseEval]

print("Load data from " + "/media/sf_lur/data/data_hour_2013.csv")

# load the data
data1 = {}
columns1 = []
loadData("/media/sf_lur/data/data_hour_2013.csv", ["location", "timestamp"], data1, columns1)

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

for p in parametersList:
    findBestFeautres(p, data1, columns1, "target")


