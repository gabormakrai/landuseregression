from data import loadFile
from Timestamp import Timestamp
from matplotlib import pyplot

# open the airquality preprocessed file
# header: location,timestamp,nox

DATA_DIRECTORY = "/media/sf_Google_Drive/transfer/data/"
OUTPUT_DIRECTORY = "/media/sf_Google_Drive/transfer/datadisc/"

data = {}

loadFile(DATA_DIRECTORY + "preprocessed/airquality.csv", data)

records = len(data["location"])

# generate statistics

avg = {}
counter = {}

for i in range(0,24):
    avg[i] = 0.0
    counter[i] = 0

for i in range(0, records):
    location = data["location"][i]
    nox = data["nox"][i]
    key = str(data["timestamp"][i])
    t = Timestamp().createBasedOnKey(key)
    avg[t.hour] = avg[t.hour] + float(nox)
    counter[t.hour] = counter[t.hour] + 1

for i in range(0,24):
    avg[i] = avg[i] / float(counter[i])
    print(str(i) + "," + str(avg[i]))

# generate the graph

hours = range(0, 24)
values = []
for h in hours:
    values.append(avg[h])

fig = pyplot.figure()
pyplot.title('Average NOx levels')
pyplot.ylabel('NOx (ug/m3)')
pyplot.xlabel('Hour')

pyplot.xlim(-1, 24)
pyplot.ylim(0.0, 100.0)

pyplot.plot(hours, values, marker='o')

pyplot.savefig(OUTPUT_DIRECTORY + "graph1.png")
