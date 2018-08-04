
def fac2Eval(targetData, predictionData):
    
    predictions_within_fac2 = 0
    
    for i in range(0, len(targetData)):
        if targetData[i] == 0:
            continue
        r = float(predictionData[i]) / float(targetData[i]) 
        if r > 0.5 and r < 2.0:
            predictions_within_fac2 = predictions_within_fac2 + 1
    
    return float(predictions_within_fac2) / float(len(targetData))
    