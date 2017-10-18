from data.data import loadData
from ex1.crossvalidation import splitDataForXValidation
from copy import deepcopy
from eval.rmse import rmseEval
from sklearn.ensemble.forest import RandomForestRegressor

OUTPUT_DATA_FILE = "/experiments/ex1/ex1_rf4.csv"

parametersList = []

for n in range(5,1000):
    for depth in [10,15,20,25,30]:
        parametersList.append({"n_estimators": n, "depth": depth})
    
locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

output = open(OUTPUT_DATA_FILE, 'w')
output.write("method,value,rmse\n")

def evalOne(parameters):
    all_obs = []
    all_pred = []
    for location in locations:
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
        if "depth" in parameters:
            model = RandomForestRegressor(max_depth = parameters["depth"], random_state=42, n_estimators=parameters["n_estimators"], n_jobs=-1)
        elif "leaf" in parameters:
            model = RandomForestRegressor(min_samples_leaf = parameters["leaf"], random_state=42, n_estimators=parameters["n_estimators"], n_jobs=-1)
        elif "max_leaf" in parameters:
            model = RandomForestRegressor(max_leaf_nodes = parameters["max_leaf"], random_state=42, n_estimators=parameters["n_estimators"], n_jobs=-1)
            
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        all_obs.extend(testY)
        all_pred.extend(prediction)
    return rmseEval(all_obs, all_pred)[1]

for p in parametersList:
    print(str(p))
    rmse = evalOne(p)
    print("\t" + str(rmse))
    if "depth" in p:
        output.write(str(p["n_estimators"]) + ",depth," + str(p["depth"]) + "," + str(rmse) + "\n")
    elif "leaf" in p:
        output.write(str(p["n_estimators"]) + ",leaf," + str(p["leaf"]) + "," + str(rmse) + "\n")
    elif "max_leaf" in p:
        output.write(str(p["n_estimators"]) + ",max_leaf," + str(p["max_leaf"]) + "," + str(rmse) + "\n")
    
output.close()
