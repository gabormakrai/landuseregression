import math

# calculating r-squared
def rsquaredEval(targetData, predictionData):
    
    averageTarget = 0.0
    
    for i in range(0, len(targetData)):
        averageTarget = averageTarget + targetData[i]

    averageTarget = averageTarget / float(len(targetData)) 
        
    SSres = 0.0
    SStot = 0.0
    for i in range(0, len(targetData)):
        SSres = SSres + math.pow(targetData[i] - predictionData[i], 2.0) 
        SStot = SStot + math.pow(targetData[i] - averageTarget, 2.0)
    
    # print("SSres:" + str(SSres) + ", SStot: " + str(SStot))
        
    rsquared = 1.0 - (SSres / SStot)
            
    return ["r2", rsquared]
