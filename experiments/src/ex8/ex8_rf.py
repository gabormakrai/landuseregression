from eval.rmse import rmseEval
from sklearn.ensemble.forest import RandomForestRegressor

def rf(week, timestampWeekCategory, stationNames, ospmData2013, ospmData2014, data2013, data2014):
    
    columns = []
    for c in data2013:
        columns.append(c)
    
    columns.remove("location")
    columns.remove("timestamp")
    columns.remove("target")
    
    X = []
    y = []
    
    for i in range(0, len(data2013["target"])):
        timestamp = str(int(data2013["timestamp"][i]))
        weekC = timestampWeekCategory[timestamp]
        if int(weekC) >= week:
            y.append(data2013["target"][i])
            x = []
            for c in columns:
                x.append(data2013[c][i])
            X.append(x)
            
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state = 42)
    model.fit(X, y)        
            
#     print(str(len(X)))

    X = []
    y = []
    
    for i in range(0, len(data2014["target"])):
        y.append(data2014["target"][i])
        x = []
        for c in columns:
            x.append(data2014[c][i])
        X.append(x)
     
    prediction = model.predict(X)
    rmse = rmseEval(y, prediction)
    return rmse
    