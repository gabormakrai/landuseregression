import math

def mgEval(targetData, predictionData):

    ln_obs = 0.0
    for i in range(0, len(targetData)):
        if targetData[i] == 0.0:
            ln_obs = ln_obs + math.log(0.001)
        else:
            ln_obs = ln_obs + math.log(targetData[i])
    ln_obs = ln_obs / float(len(targetData))
    
    ln_pred = 0.0
    for i in range(0, len(predictionData)):
        if predictionData[i] == 0.0 or predictionData[i] < 0.0: 
            ln_pred = ln_pred + math.log(0.001)
        else:
            ln_pred = ln_pred + math.log(predictionData[i])
    ln_pred = ln_pred / float(len(predictionData))

    return math.exp(ln_obs - ln_pred)
