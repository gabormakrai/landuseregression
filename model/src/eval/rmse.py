import math

# calculating rmse
def rmseEval(targetData, predictionData):
    # print(targetData)
    # print(predictionData)
    rmse = 0.0
    for i in range(0, len(targetData)):
        rmse = rmse + math.pow(targetData[i] - predictionData[i], 2.0)
    rmse = math.sqrt(rmse / float(len(targetData)))
    return rmse
