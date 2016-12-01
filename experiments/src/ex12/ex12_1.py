# generate daily weather data to pick up a couple of days for
# further investigation

import os
import json

INPUT_DIRECTORY = "/media/sf_lur/data/weather/wu/"
OUTPUT_FILE = "/media/sf_lur/experiments/ex12/weather.csv"

# load data

wData = {}
    
fileNames = next(os.walk(INPUT_DIRECTORY))[2]
        
for fileName in fileNames:
    
    absoluteFileName = INPUT_DIRECTORY + fileName
    with open(absoluteFileName, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
  
    if "history" not in data:
        continue
  
    observations = len(data['history']['observations'])
    
    for o in range(0, observations):
        hour = str(data['history']['observations'][o]['date']['hour'])
        day = str(data['history']['observations'][o]['date']['mday'])
        month = str(data['history']['observations'][o]['date']['mon'])
        year = str(data['history']['observations'][o]['date']['year'])
        timestampKey = year + month + day + hour
        
        winddirection = str(data['history']['observations'][o]['wdird'])
        windspeed = str(data['history']['observations'][o]['wspdm'])
        temperature = str(data['history']['observations'][o]['tempm'])
        rain = str(data['history']['observations'][o]['rain'])
        pressure = str(data['history']['observations'][o]['pressurem'])
        humidity = str(data['history']['observations'][o]['hum'])
        
        if pressure == "":
            continue
        if humidity == "":
            continue
        if float(pressure) < 800 or float(pressure) > 1200:
            continue
        if winddirection == "":
            continue
        if windspeed == "":
            continue
        if float(windspeed) < 0:
            continue
        if rain == "":
            continue
        try:
            float(humidity)
        except:
            continue

        wData[timestampKey] = {}
        wData[timestampKey]["winddirection"] = winddirection
        wData[timestampKey]["windspeed"] = windspeed
        wData[timestampKey]["temperature"] = temperature
        wData[timestampKey]["rain"] = rain
        wData[timestampKey]["pressure"] = pressure
        wData[timestampKey]["humidity"] = humidity

# aggregate data

dailyData = {}
for t in wData:
    
    dayTimestamp = t[:8]
        
    if dayTimestamp not in dailyData:
        dailyData[dayTimestamp] = {}
        dailyData[dayTimestamp]["winddirection"] = []
        dailyData[dayTimestamp]["windspeed"] = []
        dailyData[dayTimestamp]["temperature"] = []
        dailyData[dayTimestamp]["rain"] = []
        dailyData[dayTimestamp]["pressure"] = []
        dailyData[dayTimestamp]["humidity"] = []
     
    dailyData[dayTimestamp]["winddirection"].append(wData[t]["winddirection"])
    dailyData[dayTimestamp]["windspeed"].append(wData[t]["windspeed"])
    dailyData[dayTimestamp]["temperature"].append(wData[t]["temperature"])
    dailyData[dayTimestamp]["rain"].append(wData[t]["rain"])
    dailyData[dayTimestamp]["pressure"].append(wData[t]["pressure"])
    dailyData[dayTimestamp]["humidity"].append(wData[t]["humidity"])

timestamps = []
for ts in dailyData:
    if ts.startswith("2013"):
        timestamps.append(ts)
    
timestamps.sort()

for t in timestamps:
    print(t + " -> " + str(len(dailyData[t]["windspeed"])))

# write out csv
output = open(OUTPUT_FILE, 'w')
output.write("date,windspeed,temperature,rain,humidity\n")

for t in timestamps:
    if len(dailyData[t]["windspeed"]) < 24:
        continue
    windspeed = 0.0
    temperature = 0.0
    rain = 0.0
    humidity = 0.0
    for i in range(0, 24):
        windspeed = windspeed + float(dailyData[t]["windspeed"][i])
        temperature = temperature + float(dailyData[t]["temperature"][i])
        rain = rain + float(dailyData[t]["rain"][i])
        humidity = humidity + float(dailyData[t]["humidity"][i])
    
    windspeed = windspeed / 24.0
    temperature = temperature / 24.0
    rain = rain / 24.0
    humidity = humidity / 24.0
    
    output.write(t + ",") 
    output.write(str(windspeed) + ",") 
    output.write(str(temperature) + ",") 
    output.write(str(rain) + ",") 
    output.write(str(humidity) + "\n") 

output.close()

