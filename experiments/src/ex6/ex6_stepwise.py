import numpy as np
from data.data import loadData
from crossvalidation import findOutKForValidation, splitDataForXValidation2
from error import raeEval
from sklearn.ensemble.forest import RandomForestRegressor
from copy import deepcopy
from random import Random

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"

def loadHeader(fileName):
    with open(fileName) as infile:
        for line in infile:
            line = line.rstrip()
            headers = line.split(',')
            break
    
    headers.remove("timestamp")
    headers.remove("target")
    headers.remove("location")
    return headers

def generateForwardCases(vector, cases):
    for i in range(0, len(features)):
    #for i in range(0, 3):
        if vector[i] == 0:
            case = deepcopy(vector)
            case[i] = 1
            cases.append(case)
    
def generateBackwardCases(vector, cases):
    currentFeaturesCount = 0
    for v in vector:
        currentFeaturesCount = currentFeaturesCount + v
    if currentFeaturesCount == 1:
        return
    
    featureIndexes = []
    for i in range(0, len(vector)):
        if vector[i] == 1:
            featureIndexes.append(i)
    
    for fi in featureIndexes:
        case = deepcopy(vector)
        case[fi] = 0
        cases.append(case)
        
def convertVectorToFeatureNames(vector, features):
    res = []
    for i in range(0, len(vector)):
        if vector[i] == 1:
            res.append(features[i])
    return res

def evaluateFeatures(vector, features, data):
    featureToUse = []
    for i in range(len(vector)):
        if vector[i] == 1:
            featureToUse.append(features[i])
         
    combinedRae = []
     
    # modelling
    for location in locationValues:
         
        trainX, testX, trainY, testY = splitDataForXValidation2(location, "location", data, featureToUse, "target")
         
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state = 42)
         
        model.fit(trainX, trainY)
         
        prediction = model.predict(testX)
         
        rae = raeEval(testY, prediction)
                 
        for v in rae[1]:
            combinedRae.append(v)
             
    p50 = np.percentile(np.array(combinedRae), 50) 

    return p50

# load data
data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)
locationValues = findOutKForValidation("location", data)

print("Load features (columns) from file " + DATA_FILE)
    
features = loadHeader(DATA_FILE)

print("  Features:")
print("  " + str(features))
print("  #: " + str(len(features)))

vector = []
for i in range(0, len(features)):
    vector.append(0)

for i in range(0, len(features)):
    if features[i] == "hour":
        vector[i] = 1
        break

print("Start with only \"hour\"...")

random = Random(42)
randomSteps = 0
globalBestRes = 2.0
globalBestVector = 0

previousRes = 2.0

for step in range(0, 1000000):
    # generate the possible feature oportunities
    cases = []
    generateForwardCases(vector, cases)
    generateBackwardCases(vector, cases)
    
    result = []
    
    # random step
    if randomSteps != 0:
        nextCase = random.randint(0, len(cases) - 1)
        vector = cases[nextCase] 
        print("Random: " + str(convertVectorToFeatureNames(vector, features)))
        randomSteps = randomSteps - 1
        continue
            
    # evaluate all of them
    for case in cases:
        res = evaluateFeatures(case, features, data)
        print("  " + str(convertVectorToFeatureNames(case, features)) + " -> " + str(res))
        result.append(res)
    
    # find the best
    bestRes = 2.0
    bestVector = 0 
    for i in range(0, len(result)):
        if result[i] < bestRes:
            bestRes = result[i]
            bestVector = cases[i]
            
    # compare this to global res
    if bestRes < globalBestRes:
        globalBestRes = bestRes
        globalBestVector = bestVector
            
    # print out result
    vector = bestVector
    print("BestGlobal: " + str(convertVectorToFeatureNames(globalBestVector, features)) + " -> " + str(globalBestRes))
    print("Best: " + str(convertVectorToFeatureNames(vector, features)) + " -> " + str(bestRes))

    # compare this to previousBest
    if previousRes < bestRes:
        randomSteps = 5
        previousRes = 2.0
    else:
        previousRes = bestRes
