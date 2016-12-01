import numpy as np
import sys
from data.data import loadData
from crossvalidation import findOutKForValidation, splitDataForXValidation2
from error import raeEval
from sklearn.ensemble.forest import RandomForestRegressor

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
OUTPUT_FILE = "/media/sf_lur/experiments/ex6/" + "o4.csv"

if len(sys.argv) > 1:
    DATA_FILE = sys.argv[1]
    OUTPUT_FILE = sys.argv[2]

startPoint = 975000
endPoint = 1000000

if (len(sys.argv) > 3):
    startPoint = int(sys.argv[3])
    endPoint = int(sys.argv[4])

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

# load data
data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)
locationValues = findOutKForValidation("location", data)

print("Load features (columns) from file " + DATA_FILE)
    
features = loadHeader(DATA_FILE)

print("\tFeatures:")
print("\t" + str(features))
print("\t#: " + str(len(features)))

print("Open " + OUTPUT_FILE + " for writing...")

output = open(OUTPUT_FILE, 'w')
for f in features:
    output.write(f)
    output.write(",")
output.write("rae_0,rae_25,rae_50,rae_75,rae_100\n")

vector = []
for i in range(0, len(features)):
    vector.append(0)
vector[0] = 0
vector[1] = 0

counter = -1

print("Run modelling...")

while True:

    counter = counter + 1
    sys.stdout.write(str(counter) + " / 1048575\r")
    sys.stdout.flush()
        
    vector[0] = vector[0] + 1
    for i in range(0, len(vector) - 1):
        if vector[i] == 2:
            vector[i] = 0
            vector[i+1] = vector[i+1] + 1
    
    vectorSum = 0
    for v in vector:
        vectorSum = vectorSum + v
    if vectorSum == len(features):
        break
    
    if (startPoint <= counter and counter < endPoint) == False:
        continue
        
    featureToUse = []
    for i in range(len(vector)):
        if vector[i] == 1:
            featureToUse.append(features[i])
#     print(str(featureToUse))
        
    combinedRae = []
    
    # modelling
    for location in locationValues:
        
        trainX, testX, trainY, testY = splitDataForXValidation2(location, "location", data, featureToUse, "target")
        
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = 1)
        
        model.fit(trainX, trainY)
        
        prediction = model.predict(testX)
        
        rae = raeEval(testY, prediction)
                
        for v in rae[1]:
            combinedRae.append(v)
            
    p0 = np.percentile(np.array(combinedRae), 0) 
    p25 = np.percentile(np.array(combinedRae), 25) 
    p50 = np.percentile(np.array(combinedRae), 50) 
    p75 = np.percentile(np.array(combinedRae), 75) 
    p100 = np.percentile(np.array(combinedRae), 100)
    
    # write out result
    for v in vector:
        output.write(str(v) + ",")
        
    output.write(str(p0) + "," + str(p25) + "," + str(p50) + "," + str(p75) + "," + str(p100) + "\n")
    output.flush() 
    
print("Done...")
output.close()
