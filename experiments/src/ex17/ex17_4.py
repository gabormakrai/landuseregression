"""
Script to load Air Quality data for many years
and create graphs based on averages...
"""

from matplotlib import pyplot
from airquality import processAirQualityFiles

DATA_DIRECTORY = "/media/sf_lur/data/"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex17/"

stations = ["Bootham", "Fulford", "Gillygate", "Heworth", "Holgate", "Lawrence", "Nunnery", "Fishergate"]
years = [2012,2013,2014,2015] 

print("Loading AQ data...")

data = processAirQualityFiles(
    "no2", 
    years, 
    DATA_DIRECTORY + "stations/stations_rectangles.csv ", 
    DATA_DIRECTORY + "aq/",
    "\t"
    )

print("Done...")

avg = {}
for station in data:
    avg[station] = {}
    
for station in data:
    for year in years:
        mean = 0.0
        counter = 0
        for timestamp in data[station]:
            #print(timestamp[0:4])
            if timestamp[0:4] == str(year):
                mean = mean + data[station][timestamp]
                counter = counter + 1
        if counter > 0:
            mean = mean / float(counter)
        else:
            mean = None
        avg[station][year] = mean

for station in data:
    for year in years:
        if avg[station][year] != None:
            print(str(station) + " in " + str(year) + ": " + str(avg[station][year]))
            
fig = pyplot.figure()
ax = fig.add_subplot(111)
pyplot.title('Annual No2 levels')
pyplot.ylabel('No2 (ug/m3)')
pyplot.xlabel('Year')

#pyplot.xlim(-1, 24)
#pyplot.ylim(0.0, 130.0)

colors = ['r', 'g', 'b', '#00ffff', '#ffff00', '#ff00ff', '#88ff00', '#ff8800', '#8888ff']
colorIndex = 0

for station in data:
    values = []
    for year in years:
        if avg[station][year] != None:
            values.append(avg[station][year])
        else:
            values.append(None)
    
    ax.plot(years, values, marker='o', label = stations[int(station) - 1], color = colors[colorIndex])
    colorIndex = colorIndex + 1

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
pyplot.legend(loc='center left',  bbox_to_anchor=(1, 0.5))

pyplot.savefig(OUTPUT_DIRECTORY + "graph4.png")

