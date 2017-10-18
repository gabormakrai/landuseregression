from data.data import loadData
from ex2.crossvalidation import splitDataForXValidation
from copy import deepcopy
from sklearn.neighbors.regression import KNeighborsRegressor

OUTPUT_DATA_FILE = "/experiments/ex2/ex2_knn.csv"

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

output = open(OUTPUT_DATA_FILE, 'w')
output.write("location,observation,prediction\n")

for location in locations:
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
    model = KNeighborsRegressor(weights = "distance", n_neighbors = 23, p = 2.0)
        
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    
    for i in range(0, len(testY)):
        output.write(str(location))
        output.write(",")
        output.write(str(testY[i]))
        output.write(",")
        output.write(str(prediction[i]))
        output.write("\n")
        
output.close()        
