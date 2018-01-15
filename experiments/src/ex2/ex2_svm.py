from data.data import loadData
from ex2.crossvalidation import splitDataForXValidation
from copy import deepcopy
from sklearn.preprocessing.data import StandardScaler
from sklearn.ensemble.bagging import BaggingRegressor
from sklearn.svm.classes import SVR

OUTPUT_DATA_FILE = "/experiments/ex2/ex2_svm.csv"

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
    print(str(location))
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
    normalizer_X = StandardScaler()
    trainX = normalizer_X.fit_transform(trainX)
    testX = normalizer_X.transform(testX)
    normalizer_Y = StandardScaler()
    trainY = normalizer_Y.fit_transform(trainY)
    testY = normalizer_Y.transform(testY)
    model = BaggingRegressor(base_estimator=SVR(kernel='rbf', C=40, cache_size=5000), max_samples=4200,n_estimators=10, verbose=0, n_jobs=-1)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    prediction = normalizer_Y.inverse_transform(prediction)
    testY = normalizer_Y.inverse_transform(testY)
        
    for i in range(0, len(testY)):
        output.write(str(location))
        output.write(",")
        output.write(str(testY[i]))
        output.write(",")
        output.write(str(prediction[i]))
        output.write("\n")
        
output.close()        
