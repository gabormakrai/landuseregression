import matplotlib.pyplot as plt
import numpy as np

def loadDataOverall(fileName):
    data = {}
    
    print("Open file " + fileName + "...")
    
    firstLine = True
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:                
            # remove newline character from the end
            line = line.rstrip()
            
            # parse header
            if firstLine == True:
                firstLine = False
                continue
            
            # split the line
            splittedLine = line.split(',')
            
            group = str(splittedLine[0])
            
            if group not in data:
                data[group] = []
                
            data[group].append(float(splittedLine[1]))
            
    print("Done...")
    
    return data

def loadData(fileName):
    data = {}
    
    print("Open file " + fileName + "...")
    
    firstLine = True
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:                
            # remove newline character from the end
            line = line.rstrip()
            
            # parse header
            if firstLine == True:
                firstLine = False
                continue
            
            # split the line
            splittedLine = line.split(',')
            
            group = str(splittedLine[0])
            
            if group not in data:
                data[group] = {}
                
            hour = str(splittedLine[1])
            if hour not in data[group]:
                data[group][hour] = []
                
            data[group][hour].append(float(splittedLine[2]))
            
    print("Done...")
    
    return data
            
inputFile1 = "/media/sf_lur/data_significance/result_rfr.csv"            
inputFile2 = "/media/sf_lur/data_significance/result_hour_rfr.csv"
outputFile1 = "/media/sf_lur/data_significance/graph_hour_rfr_1_"
outputFile2 = "/media/sf_lur/data_significance/graph_hour_rfr_2.png"
outputFile3 = "/media/sf_lur/data_significance/graph_hour_rfr_3.png"

overallData = loadDataOverall(inputFile1)

data = loadData(inputFile2)

# for hour in range(0, 24):
# 
#     fig = plt.figure(None, figsize=(40, 20))
#     ax = fig.add_subplot(111)
#     
#     dataToPlot = []
#     
#     groups = []
#     
#     for group in data:
#         groups.append(group)
#         
#     groups.sort()
#     
#     for group in groups:
#         groupData = data[group][str(hour)]
#         zero = False
#         for i in range(0, len(groupData)):
#             if groupData[i] > 300.0:
#                 zero = True
#         if zero:
#             for i in range(0, len(groupData)):
#                 groupData[i] = 0.0
#         
#         dataToPlot.append(groupData)
#         print(str(group) + " -> " + str(len(groupData)))
#     
#     
#     ax.boxplot(dataToPlot, showfliers=False)
#     ax.set_xticklabels(groups, rotation='vertical')
#     plt.ylim(0.0, 30.0)
#     
#     plt.savefig(outputFile1 + str(hour) + ".png")
# 
# fig = plt.figure(None, figsize=(10, 14))
# ax = fig.add_subplot(111)
#  
# dataWithoutTimeWeather = []
# dataWithTime = []
# dataWithWeather = []
# dataWithTimeWeather = []
# 
# dataWithoutTimeWeatherDay = []
# dataWithTimeDay = []
# dataWithWeatherDay = []
# dataWithTimeWeatherDay = []
# 
# dataWithoutTimeWeatherNight = []
# dataWithTimeNight = []
# dataWithWeatherNight = []
# dataWithTimeWeatherNight = []
# 
# groups = []
# for group in data:
#     groups.append(group)
# 
# for group in groups:
#     groupData = overallData[group]
#             
#     for v in groupData:
#         if "we0ti0" in group:
#             dataWithoutTimeWeather.append(v)
#         elif "we1ti0" in group:
#             dataWithWeather.append(v)
#         elif "we0ti1" in group:
#             dataWithTime.append(v)
#         else:
#             dataWithTimeWeather.append(v)
#  
# for group in groups:
#     groupData = data[group]
#     
#     for hour in groupData:
#         
#         if int(hour) < 6 or int(hour) > 20:
#             for v in groupData[hour]:
#                 if "we0ti0" in group:
#                     dataWithoutTimeWeatherNight.append(v)
#                 elif "we1ti0" in group:
#                     dataWithWeatherNight.append(v)
#                 elif "we0ti1" in group:
#                     dataWithTimeNight.append(v)
#                 else:
#                     dataWithTimeWeatherNight.append(v)
#         else:
#             for v in groupData[hour]:
#                 if "we0ti0" in group:
#                     dataWithoutTimeWeatherDay.append(v)
#                 elif "we1ti0" in group:
#                     dataWithWeatherDay.append(v)
#                 elif "we0ti1" in group:
#                     dataWithTimeDay.append(v)
#                 else:
#                     dataWithTimeWeatherDay.append(v)
#              
# print("dataWithoutTimeWeather: " + str(len(dataWithoutTimeWeather)))
# print("dataWithWeather: " + str(len(dataWithWeather)))
# print("dataWithTime: " + str(len(dataWithTime)))
# print("dataWithTimeWeather: " + str(len(dataWithTimeWeather)))
# 
# print("dataWithoutTimeWeatherDay: " + str(len(dataWithoutTimeWeatherDay)))
# print("dataWithWeatherDay: " + str(len(dataWithWeatherDay)))
# print("dataWithTimeDay: " + str(len(dataWithTimeDay)))
# print("dataWithTimeWeatherDay: " + str(len(dataWithTimeWeatherDay)))
# 
# print("dataWithoutTimeWeatherNight: " + str(len(dataWithoutTimeWeatherNight)))
# print("dataWithWeatherNight: " + str(len(dataWithWeatherNight)))
# print("dataWithTimeNight: " + str(len(dataWithTimeNight)))
# print("dataWithTimeWeatherNight: " + str(len(dataWithTimeWeatherNight)))
#  
# dataToPlot = [
#     dataWithoutTimeWeather, dataWithoutTimeWeatherDay, dataWithoutTimeWeatherNight,
#     dataWithWeather, dataWithWeatherDay, dataWithWeatherNight,
#     dataWithTime, dataWithTimeDay, dataWithTimeNight,
#     dataWithTimeWeather, dataWithTimeWeatherDay, dataWithTimeWeatherNight
#     ] 
# 
# names = [
#     "w/o TW", "w/o TW (day)","w/o TW (night)",
#     "w/ W", "w/ W (day)", "w/ W (night)",
#     "w/ T", "w/ T (day)", "w/ T (night)",
#     "w/ T+W", "w/ T+W (day)", "w/ T+W (night)"
#     ]
# 
# ax.boxplot(dataToPlot, showfliers=False)
# ax.set_xticklabels(names, rotation='vertical')
# plt.ylim(0.0, 30.0)
#  
# plt.savefig(outputFile2)
 
fig = plt.figure(None, figsize=(12, 18))
ax = fig.add_subplot(111)
 
# referenceData = overallData["lu0to0ts0td0we1ti1"]
# dataToPlot = []
# groupNames = []

referenceDataDay = []
referenceDataNight = []

# create reference data
for hour in range(0,24):
    if int(hour) < 6 or int(hour) > 20:
        for v in data["lu0to0ts0td0we1ti1"][str(hour)]:
            referenceDataNight.append(v)
    else:
        for v in data["lu0to0ts0td0we1ti1"][str(hour)]:
            referenceDataDay.append(v)
    
# print(str(referenceDataDay))
# print(str(len(referenceDataDay)))    
# print(str(referenceDataNight))    
# print(str(len(referenceDataNight)))

groupsOrdered = []
for group in data:
    groupsOrdered.append(group)
groupsOrdered.sort()

dataToPlot = []
names = []

for group in groupsOrdered:
     
    groupData = data[group]

    # if it is the reference then skip it                  
    if group == "lu0to0ts0td0we1ti1":
        continue

    # if it does not contain Time or Weather data then skip it      
    if "we1ti1" not in group:
        continue
    
    # create the data array
    dataDay = []
    dataNight = []
    
    for hour in range(0,24):
        if int(hour) < 6 or int(hour) > 20:
            for v in groupData[(str(hour))]:
                dataNight.append(v)
        else:
            for v in groupData[(str(hour))]:
                dataDay.append(v)
    
    # generate error rates from pure numbers
    for i in range(0, len(dataDay)):
        dataDay[i] = 1.0 + (dataDay[i] - referenceDataDay[i]) / referenceDataDay[i]
    for i in range(0, len(dataNight)):
        dataNight[i] = 1.0 + (dataNight[i] - referenceDataNight[i]) / referenceDataNight[i]
        
    names.append(group[0:12] + "(night)")
    dataToPlot.append(dataNight)
    names.append(group[0:12] + "(day)")
    dataToPlot.append(dataDay)
    
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')
plt.ylim(0.5, 2.0)
  
plt.savefig(outputFile3)

