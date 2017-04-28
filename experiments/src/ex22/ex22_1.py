from data.data import loadData
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from crossvalidation import findOutKForValidation

DATA_FILE = "/media/sf_lur/data_london/data_hour_2015.csv"

data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)

#locations = findOutKForValidation("location", data)
locations = ['61.0', '66.0', '64.0']

print(str(columns))


# modelling
for location in locations:
    loc = float(location)
    print("location: " + str(location)) 
    trainX, testX, trainY, testY = splitDataForXValidation(loc, "location", data, columns, "target")
    print("\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 20, n_estimators = 59, n_jobs = -1, random_state=42, max_samples=0.5)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))

