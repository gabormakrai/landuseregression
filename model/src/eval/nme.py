# import math
# 
# # calculating nme
# def nmseEval(targetData, predictionData):
#     # print(targetData)
#     # print(predictionData)
#     nmse = 0.0
#     avgTarget = 0.0
#     for i in range(0, len(targetData)):
#         nmse = nmse + abs(targetData[i] - predictionData[i])
#         avgTarget = avgTarget + targetData[i]
#     
#     avgTarget = avgTarget / float(len(targetData))
#     nmse = nmse / (len(targetData) * avgTarget * avgPrediction)
#     if nmse > 1.0:
#         print("NMSE larger then 1.0")
#         print("avgTarget: " + str(avgTarget))
#         print("avgPrediction: " + str(avgPrediction))
#         print("original nmse: " + str(nmse1))
#         print("len(targetData): " + str(len(targetData)))
#     return ["nmse", nmse]
