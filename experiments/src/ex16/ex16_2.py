from data.data import loadData
from crossvalidation import findOutKForValidation, splitDataForXValidation2
from sklearn.ensemble.forest import RandomForestRegressor
from copy import deepcopy
from eval.rmse import rmseEval

DATA_FILE = "/media/sf_lur/data/" + "data3_hour_2013.csv"

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
         
    combinedRmse = []
     
    # modelling
    for location in locationValues:
         
        trainX, testX, trainY, testY = splitDataForXValidation2(location, "location", data, featureToUse, "target")
         
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state = 42)
         
        model.fit(trainX, trainY)
         
        prediction = model.predict(testX)

        rmse = rmseEval(testY, prediction)
        
        combinedRmse.append(rmse[1])
         
    # calculate avg rmse
    
    avgRmse = 0.0
    for rmse in combinedRmse:
        avgRmse = avgRmse + rmse

    avgRmse = avgRmse / len(combinedRmse)

    return avgRmse

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

for step in range(0, 1000):
    # generate the possible feature oportunities
    cases = []
    generateForwardCases(vector, cases)
    generateBackwardCases(vector, cases)
    
    result = []
            
    # evaluate all of them
    for case in cases:
        res = evaluateFeatures(case, features, data)
        print("  " + str(convertVectorToFeatureNames(case, features)) + " -> " + str(res))
        result.append(res)
    
    # find the best
    bestRes = 100000
    bestVector = 0 
    for i in range(0, len(result)):
        if result[i] < bestRes:
            bestRes = result[i]
            bestVector = cases[i]
            
    # print out result
    vector = bestVector
    print("Best: " + str(convertVectorToFeatureNames(vector, features)) + " -> " + str(bestRes))

