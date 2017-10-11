from data.data import loadData
from ex1.crossvalidation import splitDataForXValidation
from copy import deepcopy
from eval.rmse import rmseEval
from sklearn.ensemble.bagging import BaggingRegressor
from sklearn.svm.classes import SVR
from sklearn.preprocessing.data import StandardScaler

OUTPUT_DATA_FILE = "/experiments/ex1/ex1_svm2.csv"

parametersList = []
for c in range(1,100):
    for samples in [i * 50 for i in range(1,201)]:
        parametersList.append({"C": c, "max_samples": samples, "n_estimators": 10})

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

output = open(OUTPUT_DATA_FILE, 'w')
output.write("n_estimators,C,max_samples,rmse\n")

def evalOne(parameters):
    all_obs = []
    all_pred = []
    for location in locations:
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
        normalizer_X = StandardScaler()
        trainX = normalizer_X.fit_transform(trainX)
        testX = normalizer_X.transform(testX)
        normalizer_Y = StandardScaler()
        trainY = normalizer_Y.fit_transform(trainY)
        testY = normalizer_Y.transform(testY)
        model = BaggingRegressor(base_estimator=SVR(kernel='rbf', C=parameters["C"], cache_size=5000), max_samples=parameters["max_samples"],n_estimators=parameters["n_estimators"], verbose=0, n_jobs=-1)
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        prediction = normalizer_Y.inverse_transform(prediction)
        testY = normalizer_Y.inverse_transform(testY)
        all_obs.extend(testY)
        all_pred.extend(prediction)
        
    return rmseEval(all_obs, all_pred)[1]

for p in parametersList:
    print(str(p))
    rmse = evalOne(p)
    print("\t" + str(rmse))
    output.write(str(p["n_estimators"]) + "," + str(p["C"]) + "," + str(p["max_samples"]) + "," + str(rmse) + "\n")
    output.flush()
    
output.close()
