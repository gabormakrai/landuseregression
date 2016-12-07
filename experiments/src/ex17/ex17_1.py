from matplotlib import pyplot
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

avg = {}
counter = {}

for i in range(0,24):
    avg[i] = 0.0
    counter[i] = 0

for i in range(0, records):
    location = data["location"][i]
    no2 = data["target"][i]
    key = str(int(data["timestamp"][i]))
    h = int(key[8:10])
    avg[h] = avg[h] + float(no2)
    counter[h] = counter[h] + 1

for i in range(0,24):
    avg[i] = avg[i] / float(counter[i])
    print(str(i) + "," + str(avg[i]))

# generate the graph

hours = range(0, 24)
values = []
for h in hours:
    values.append(avg[h])

fig = pyplot.figure()
pyplot.title('Average No2 levels')
pyplot.ylabel('No2 (ug/m3)')
pyplot.xlabel('Hour')

pyplot.xlim(-1, 24)
pyplot.ylim(0.0, 100.0)

pyplot.plot(hours, values, marker='o')

pyplot.savefig(OUTPUT_DIRECTORY + "graph1.png")
