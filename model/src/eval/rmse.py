import math

# calculating rmse
def rmseEval(data, target, prediction):
    targetData = data[target]
    predictionData = data[prediction]
    rmse = 0
    for i in range(0, len(targetData)):
        rmse = rmse + math.pow(targetData[i] - predictionData[i], 2.0)
    rmse = math.sqrt(rmse)
    return rmse
