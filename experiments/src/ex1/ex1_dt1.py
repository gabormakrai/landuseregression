from data.data import loadData
from ex1.crossvalidation import splitDataForXValidation
from copy import deepcopy
from eval.rmse import rmseEval
from sklearn.tree.tree import DecisionTreeRegressor

OUTPUT_DATA_FILE = "/experiments/ex1/ex1_dt1.csv"

parametersList = []

for depth in range(2,150):
    parametersList.append({"depth": depth})
for leaf in range(2,150):
    parametersList.append({"leaf": leaf})
for max_leaf in range(2,150):
    parametersList.append({"max_leaf": max_leaf})
    
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
            model = DecisionTreeRegressor(max_depth = parameters["depth"], random_state=42)
        elif "leaf" in parameters:
            model = DecisionTreeRegressor(min_samples_leaf = parameters["leaf"], random_state=42)
        elif "max_leaf" in parameters:
            model = DecisionTreeRegressor(max_leaf_nodes = parameters["max_leaf"], random_state=42)
            
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
        output.write("depth," + str(p["depth"]) + "," + str(rmse) + "\n")
    elif "leaf" in p:
        output.write("leaf," + str(p["leaf"]) + "," + str(rmse) + "\n")
    elif "max_leaf" in p:
        output.write("max_leaf," + str(p["max_leaf"]) + "," + str(rmse) + "\n")
    
output.close()
