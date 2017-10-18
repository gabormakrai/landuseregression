from data.data import loadData
from ex1.crossvalidation import splitDataForXValidation
from copy import deepcopy
from eval.rmse import rmseEval
from sklearn.neighbors.regression import KNeighborsRegressor

OUTPUT_DATA_FILE = "/experiments/ex1/ex1_knn1.csv"

parametersList = []
for d in ["distance", "uniform"]:
    for p in [1.0, 2.0, 3.0, 4.0]:
        for n in range(2, 100):
            parametersList.append({"p": p, "neighbors": n, "weights": d})

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

output = open(OUTPUT_DATA_FILE, 'w')
output.write("weights,p,neighbours,rmse\n")

def evalOne(parameters):
    
    all_obs = []
    all_pred = []
#     all_obs_train = []
#     all_pred_train = []

    for location in locations:
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
        model = KNeighborsRegressor(weights = parameters["weights"], n_neighbors = parameters["neighbors"], p = parameters["p"])
        model.fit(trainX, trainY)
#         train_prediction = model.predict(trainX)
        prediction = model.predict(testX)
        all_obs.extend(testY)
        all_pred.extend(prediction)
#         all_obs_train.extend(trainY)
#         all_pred_train.extend(train_prediction)

    return rmseEval(all_obs, all_pred)[1] 

for p in parametersList:
    print(str(p))
    rmse = evalOne(p)
    print("\t" + str(rmse))
    output.write(str(p["weights"]) + "," + str(p["p"]) + "," + str(p["neighbors"]) + "," + str(rmse) + "\n")
    
output.close()
