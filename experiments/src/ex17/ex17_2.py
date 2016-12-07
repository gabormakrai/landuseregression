from matplotlib import pyplot
from datetime import datetime
from data.data import loadData

# open the airquality preprocessed file
# header: location,timestamp,nox

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex17/"

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

records = len(data["location"])

# generate statistics

avg1 = {}
counter1 = {}
avg2 = {}
counter2 = {}

for i in range(0,24):
    avg1[i] = 0.0
    counter1[i] = 0
    avg2[i] = 0.0
    counter2[i] = 0

for i in range(0, records):
    location = data["location"][i]
    no2 = data["target"][i]
    key = str(int(data["timestamp"][i]))
    year = int(key[0:4])
    month = int(key[4:6])
    day = int(key[6:8])
    hour = int(key[8:10])
    d = datetime(year, month, day)
    dayOfWeek = int(d.weekday())
    
    if dayOfWeek < 5:
        avg1[hour] = avg1[hour] + float(no2)
        counter1[hour] = counter1[hour] + 1
    else:
        avg2[hour] = avg2[hour] + float(no2)
        counter2[hour] = counter2[hour] + 1
        
for i in range(0,24):
    avg1[i] = avg1[i] / float(counter1[i])
    avg2[i] = avg2[i] / float(counter2[i])

# generate the graphs

hours = range(0, 24)
values1 = []
values2 = []
for h in hours:
    values1.append(avg1[h])
    values2.append(avg2[h])

fig = pyplot.figure()
pyplot.title('Average No2 levels')
pyplot.ylabel('No2 (ug/m3)')
pyplot.xlabel('Hour')

pyplot.xlim(-1, 24)
pyplot.ylim(0.0, 130.0)

pyplot.plot(hours, values1, marker='o', label = "weekdays")
pyplot.plot(hours, values2, marker='o', color='red', label = "weekends")

pyplot.legend(loc='best')

pyplot.savefig(OUTPUT_DIRECTORY + "graph2.png")
