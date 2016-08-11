import math

# calculating nmse
def nmseEval(targetData, predictionData):
    # print(targetData)
    # print(predictionData)
    nmse = 0.0
    avgTarget = 0.0
    avgPrediction = 0.0
    for i in range(0, len(targetData)):
        nmse = nmse + math.pow(targetData[i] - predictionData[i], 2.0)
        avgTarget = avgTarget + targetData[i]
        avgPrediction = avgPrediction + predictionData[i]
    
    avgTarget = avgTarget / float(len(targetData))
    avgPrediction = avgPrediction / float(len(targetData))
#     nmse1 = nmse
    nmse = nmse / (len(targetData) * avgTarget * avgPrediction)
#     if nmse > 1.0:
#         print("NMSE larger then 1.0")
#         print("avgTarget: " + str(avgTarget))
#         print("avgPrediction: " + str(avgPrediction))
#         print("original nmse: " + str(nmse1))
#         print("len(targetData): " + str(len(targetData)))
    return ["nmse", nmse]
