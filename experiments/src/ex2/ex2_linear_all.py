from data.data import loadData
from ex2.crossvalidation import splitDataForXValidation
from copy import deepcopy
from sklearn import linear_model

OUTPUT_DATA_FILE = "/experiments/ex2/ex2_linear_all.csv"

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

# remove to decrease rmse from 10000000.0... 
all_features.remove('buildings_area')
all_features.remove('leisure_area')

output = open(OUTPUT_DATA_FILE, 'w')
output.write("location,observation,prediction\n")

for location in locations:
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
    model = linear_model.LinearRegression(True, True, True, -1)
        
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
