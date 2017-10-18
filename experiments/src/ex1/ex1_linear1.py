from data.data import loadData
from sklearn import linear_model
from ex1.crossvalidation import splitDataForXValidation
from copy import deepcopy
from eval.rmse import rmseEval

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

print(str(columns))

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

# remove to decrease rmse from 10000000.0... 
all_features.remove('buildings_area')
all_features.remove('leisure_area')

all_obs = []
all_pred = []

for location in locations:
    print("Location: " + str(location))
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
    model = linear_model.LinearRegression(True, True, True, -1)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = str(rmseEval(testY, prediction)[1])
    print("\tRmse:" + rmse)
    all_obs.extend(testY)
    all_pred.extend(prediction)

print("Overall:")
rmse = str(rmseEval(all_obs, all_pred)[1])
print("Rmse:" + rmse)
