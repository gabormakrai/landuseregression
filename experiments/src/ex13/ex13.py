import numpy as np
from data.data import loadData
from crossvalidation import findOutKForValidation, splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from copy import deepcopy
from error import raeEval

stationNames = {}
stationNames["2.0"] = "Fulford"
stationNames["3.0"] = "Gillygate"
stationNames["4.0"] = "Heworth"
stationNames["5.0"] = "Holgate"
stationNames["6.0"] = "Lawrence"
stationNames["7.0"] = "Nunnery"
stationNames["8.0"] = "Fishergate"

DATA_FILE = "/data/york3_hour_2013.csv"
DATA_FILE2 = "/data/york_hour_2013.csv"

# load data
data = {}
columns = []
loadData(DATA_FILE, ["timestamp"], data, columns)
locationValues = findOutKForValidation("location", data)

# load normal data (not data with atc...)

data2 = {}
columns2 = []
loadData(DATA_FILE2, ["timestamp"], data2, columns2)

featureTW = []

# weather related
featureTW.append('winddirection')
featureTW.append('windspeed')
featureTW.append('temperature')
featureTW.append('rain')
featureTW.append('pressure')

# time related
featureTW.append('hour')
featureTW.append('day_of_week')
featureTW.append('month')
featureTW.append('bank_holiday')
featureTW.append('race_day')

#atc feature
featureTWAtc = deepcopy(featureTW)
featureTWAtc.append("atc")

# modelling
for location in locationValues:
    
    print("location: " + stationNames[str(location)])
    
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data2, featureTW, "target")
    print("\tT+W (on data without ATC) #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    rae = raeEval(testY, prediction)[1]
    p50 = np.percentile(np.array(rae), 50) 
    print("\tmean of RAE: " + str(p50))
    
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, featureTW, "target")
    print("\tT+W #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    rae = raeEval(testY, prediction)[1]
    p50 = np.percentile(np.array(rae), 50) 
    print("\tmean of RAE: " + str(p50))
                  
    trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, featureTWAtc, "target")
    print("\tT+W+Atc #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))
    rae = raeEval(testY, prediction)[1]
    p50 = np.percentile(np.array(rae), 50) 
    print("\tmean of RAE: " + str(p50))
    