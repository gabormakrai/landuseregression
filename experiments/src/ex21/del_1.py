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
locations = ['61.0', '66.0', '64.0', '25.0', '1.0', '36.0', '4.0', '59.0', '56.0', '3.0', '62.0', '34.0', '77.0', '18.0', '22.0', '71.0', '5.0', '75.0', '10.0', '21.0', '69.0', '60.0', '27.0', '2.0', '41.0', '80.0', '52.0', '47.0', '74.0', '39.0', '58.0', '37.0', '28.0', '63.0', '23.0', '92.0', '38.0', '67.0', '70.0', '31.0', '15.0', '82.0', '29.0', '57.0', '93.0', '87.0', '24.0', '68.0', '86.0', '35.0', '26.0', '12.0', '81.0', '53.0', '20.0', '55.0', '65.0', '6.0', '17.0', '49.0', '54.0', '48.0', '40.0', '79.0', '91.0', '43.0', '76.0', '14.0', '9.0', '78.0', '73.0', '19.0', '32.0', '42.0', '46.0', '30.0', '85.0', '45.0', '50.0', '8.0', '72.0', '33.0', '16.0', '11.0', '88.0', '84.0', '44.0', '7.0', '13.0', '90.0', '83.0', '89.0', '51.0']


# modelling
for location in locations:
    loc = float(location)
    print("location: " + str(location)) 
    trainX, testX, trainY, testY = splitDataForXValidation(loc, "location", data, columns, "target")
    print("\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    rmse = rmseEval(testY, prediction)[1]
    print("\trmse: " + str(rmse))

#     
#     trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data2, featureTWAtc, "target", timestampData2)                  
#     print("\tT+W+Atc #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
#     model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
#     model.fit(trainX, trainY)
#     prediction = model.predict(testX)
#     rmse = rmseEval(testY, prediction)[1]
#     print("\trmse: " + str(rmse))
#     for i in range(0, len(testY)):
#         timestamp = testTimestamp[i]
#         value = prediction[i]
#         TWAtcpredictionData[str(location)][timestamp] = value
#         
#     trainX, testX, trainY, testY, trainTimestamp, testTimestamp = splitDataForXValidation(location, "location", data2, featureWAtc, "target", timestampData2)                  
#     print("\tW+Atc #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
#     model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
#     model.fit(trainX, trainY)
#     prediction = model.predict(testX)
#     rmse = rmseEval(testY, prediction)[1]
#     print("\trmse: " + str(rmse))
#     for i in range(0, len(testY)):
#         timestamp = testTimestamp[i]
#         value = prediction[i]
#         WAtcpredictionData[str(location)][timestamp] = value
#         
# minValues = {}
# maxValues = {}
# for c in featureTWAtc:
#     minV = float("+inf")
#     maxV = float("-inf")
#     for v in data2[c]:
#         if minV > v:
#             minV = v
#         if maxV < v:
#             maxV = v
#     minValues[c] = minV
#     maxValues[c] = maxV
#     print(str(c) + " -> min: " + str(minV) + ", max: " + str(maxV))
# 
# minValues["windspeed"] = 0.0
#         
# for (station, day) in daysInInterest:
#     stationId = 0.0
#     for sId in stationNames:
#         if stationNames[sId] == station:
#             stationId = sId
#             break
#     timestamps = generateTimestampsForADay(day)
#     
#     dayObs = []
#     dayTW = []
#     dayTWA = []
#     dayWA = []
#     for timestamp in timestamps:
#         dayObs.append(observationData[str(stationId)][timestamp])
#         dayTW.append(TWpredictionData[str(stationId)][timestamp])
#         dayTWA.append(TWAtcpredictionData[str(stationId)][timestamp])
#         dayWA.append(WAtcpredictionData[str(stationId)][timestamp])
#     
#     names = []
#     dData = []
#         
#     names.append("T+W")
#     dData.append(dayTW)
#     
#     names.append("T+W+A")
#     dData.append(dayTWA)
#     
#     names.append("W+A")
#     dData.append(dayWA)
#     
#     names.append("Observation")
#     dData.append(dayObs)
#     
#     names2 = []
#     dData2 = []
#     
#     names2.append("error(T+W)")
#     d = []
#     for i in range(0, len(dayObs)):
#         d.append(abs(dayTW[i] - dayObs[i]))
#     dData2.append(d)
#     
#     names2.append("error(T+W+A)")
#     d = []
#     for i in range(0, len(dayObs)):
#         d.append(abs(dayTWA[i] - dayObs[i]))
#     dData2.append(d)
#     
#     names2.append("error(W+A)")
#     d = []
#     for i in range(0, len(dayObs)):
#         d.append(abs(dayWA[i] - dayObs[i]))
#     dData2.append(d)
#     
# #     names2.append("diff")
# #     d = []
# #     for i in range(0, len(dayObs)):
# #         d.append(dData2[0][i] - dData2[1][i])
# #     dData2.append(d)
#     
#     names3 = []
#     dData3 = []
#     for c in featureTWAtc:
#         minV = minValues[c]
#         maxV = maxValues[c]
#         names3.append(c)
#         d = []
#         foundRecord = False
#         for timestamp in timestamps:
#             for i in range(0, len(data2["timestamp"])):
#                 if str(float(timestamp)) == str(data2["timestamp"][i]) and str(data2["location"][i]) == str(stationId):
#                     value = data2[c][i]
#                     value = (value - minV) / (maxV - minV)
#                     d.append(value)
#                     foundRecord = True
#                     break
#             if foundRecord == False:
#                 d.append(float("nan"))
#         dData3.append(d)
#     
#     doLineChart(OUTPUT_DIRECTORY + station.lower() + "_" + day + ".png", "No2 prediction @ " + station + " @ " + day, dData, names, dData2, names2, dData3, names3)
#          
#     names2.append("e(T+W)-e(T+W+A)")
#     d = []
#     for i in range(0, 24):
#         v = dData2[0][i] - dData2[1][i]
#         d.append(v)
#     dData2.append(d)
#     
#     names2.append("e(T+W)-e(W+A)")
#     d = []
#     for i in range(0, 24):
#         v = dData2[0][i] - dData2[2][i]
#         d.append(v)
#     dData2.append(d)
#     
#     doBoxplot(OUTPUT_DIRECTORY + station.lower() + "_" + day + "b.png", "No2 prediction errors @ " + station + " / " + day, "conc. level (ug/m3)", dData2, names2)
