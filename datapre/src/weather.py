import json
from urllib.request import urlopen
from rectangles import loadRectangles, Station
from time import sleep
import os

def processWeatherFile(inputFile, inputRectangleFile, outputFile, printPrefixString):
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    print(printPrefixString + "Writing out weather data to " + outputFile + "...")
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,winddirection,windspeed,temperature,humidity,pressure\n")

    firstLine = True
    # open the file
    with open(inputFile) as infile:
        # read line by line
        for line in infile:
            # skip the first line (header line)
            
            if firstLine == True:
                firstLine = False
                continue
            
            # remove newline character from the end
            line = line.rstrip()
            
            # split the line
            splittedLine = line.split(',')
            
            for rectangle in rectangles:
                output.write(str(rectangle.ID))
                output.write(",")
                output.write(splittedLine[0])
                output.write(",")
                output.write(splittedLine[1])
                output.write(",")
                output.write(splittedLine[2])
                output.write(",")
                output.write(splittedLine[3])
                output.write(",")
                output.write(splittedLine[4])
                output.write(",")
                output.write(splittedLine[5])
                output.write("\n")

    output.close()

    print(printPrefixString + "Done...")
    
def processWeatherFileBinned(inputFile, inputRectangleFile, outputFile, printPrefixString):
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    print(printPrefixString + "Writing out weather data to " + outputFile + "...")
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,")
    for i in range(0, 12):
        output.write("winddirection" + str(i) + ",")
    for i in range(0, 8):
        output.write("windspeed" + str(i) + ",")
    for i in range(0, 6):
        output.write("temperature" + str(i) + ",")
    for i in range(0, 10):
        output.write("humidity" + str(i) + ",")
    for i in range(0, 8):
        output.write("pressure" + str(i))
        if i == 7:
            output.write("\n")
        else:
            output.write(",")

    firstLine = True
    # open the file
    with open(inputFile) as infile:
        # read line by line
        for line in infile:
            # skip the first line (header line)
            
            if firstLine == True:
                firstLine = False
                continue
            
            # remove newline character from the end
            line = line.rstrip()
            
            # split the line
            splittedLine = line.split(',')
            
            for rectangle in rectangles:
                output.write(str(rectangle.ID))
                output.write(",")
                output.write(splittedLine[0])
                output.write(",")
                # winddirection (30 degrees -> 12 variables)
                category = int(float(splittedLine[1]) / 30.0)
                for i in range(0, 12):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # windspeed (5 m/s bins -> 8 variables)
                category = int(float(splittedLine[2]) / 5.0)
                for i in range(0, 8):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # temperature (6 celsius degrees -> 6 variables)
                category = int(float(splittedLine[3]) / 5.0)
                for i in range(0, 6):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # humidity
                category = int(float(splittedLine[4]) / 10.0)
                for i in range(0, 10):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # pressure
                category = int((float(splittedLine[5]) - 955.0) / 10.0)
                for i in range(0, 8):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    if i == 7:
                        output.write("\n")
                    else:
                        output.write(",")

    output.close()

    print(printPrefixString + "Done...")

def downloadWeatherDataFromWunderground(apiKey, country, city, dates, outputDirectory, sleepTime, printPrefixString = ""):
    for d in dates:
        outputFile = outputDirectory + city.lower() + "_" + d + ".json"
        # if outputFile exist then skip the process
        if os.path.isfile(outputFile):
            print(printPrefixString + "File " + outputFile + " does exist...")
        else:
            url = "http://api.wunderground.com/api/" + apiKey + "/history_" + d + "/q/" + country + "/" + city + ".json"
            print(printPrefixString + "Downloading " + url + "...")
            response = urlopen(url).read().decode("utf-8")
            data = str(response)
            print(printPrefixString + "Saving date to " + outputFile + "...")
            output = open(outputFile, 'w')
            output.write(data)
            output.close()
            print(printPrefixString + "Done...")
            sleep(sleepTime)

def downloadWeatherDataFromWundergroundWithCoordinates(apiKeys, latitude, longitude, dates, filePrefix, sleepTime, printPrefixString = ""):
    keyIndex = 0
    for d in dates:
        outputFile = filePrefix + d + ".json"
        # if outputFile exist then skip the process
        if os.path.isfile(outputFile):
            print(printPrefixString + "File " + outputFile + " does exist...")
        else:
            apiKey = apiKeys[keyIndex]
            keyIndex = (keyIndex + 1) % len(apiKeys)
            url = "http://api.wunderground.com/api/" + apiKey + "/history_" + d + "/q/" + str(latitude) + "," + str(longitude) + ".json"
            print(printPrefixString + "Downloading " + url + "...")
            response = urlopen(url).read().decode("utf-8")
            data = str(response)
            print(printPrefixString + "Saving date to " + outputFile + "...")
            output = open(outputFile, 'w')
            output.write(data)
            output.close()
            print(printPrefixString + "Done...")
            sleep(sleepTime)

def downloadWeatherForecastFromWunderground(apiKey, country, city, outputFile, sleepTime, printPrefixString = ""):
    url = "http://api.wunderground.com/api/" + apiKey + "/hourly10day/q/" + country + "/" + city + ".json"
    print(printPrefixString + "Downloading " + url + "...")
    response = urlopen(url).read().decode("utf-8")
    data = str(response)
    print(printPrefixString + "Saving date to " + outputFile + "...")
    output = open(outputFile, 'w')
    output.write(data)
    output.close()
    print(printPrefixString + "Done...")
    sleep(sleepTime)

def processWUData(timestamps, inputDirectory, rectangleFile, outputFile, printPrefixString = "", fileList = None, binned=False):
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, rectangleFile, printPrefixString)
    
    weatherData = {}
    
    if fileList == None:
        fileNames = next(os.walk(inputDirectory))[2]
    else:
        fileNames = fileList
        
    for fileName in fileNames:
        
        absoluteFileName = inputDirectory + fileName
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
            
            weatherData[timestampKey] = {}
            weatherData[timestampKey]['winddirection'] = winddirection
            weatherData[timestampKey]['windspeed'] = windspeed
            weatherData[timestampKey]['temperature'] = temperature
            weatherData[timestampKey]['rain'] = rain
            weatherData[timestampKey]['pressure'] = pressure
            weatherData[timestampKey]['humidity'] = humidity
            
    output = open(outputFile, 'w')
    if binned==False:
        output.write("location,timestamp,winddirection,windspeed,temperature,humidity,rain,pressure\n")
    else:
        output.write("location,timestamp,")
        for i in range(0, 12):
            output.write("winddirection" + str(i) + ",")
        for i in range(0, 8):
            output.write("windspeed" + str(i) + ",")
        for i in range(0, 6):
            output.write("temperature" + str(i) + ",")
        for i in range(0, 10):
            output.write("humidity" + str(i) + ",")
        for i in range(0,2):
            output.write("rain" + str(i) + ",")
        output.write("pressure0")
        for i in range(1, 8):
            output.write(",pressure" + str(i))
        output.write("\n")
    
    for timestamp in timestamps:
        if timestamp.key not in weatherData:
            continue
        if weatherData[timestamp.key]['pressure'] == "":
            continue
        if weatherData[timestamp.key]['humidity'] == "":
            continue
        if float(weatherData[timestamp.key]['pressure']) < 800 or float(weatherData[timestamp.key]['pressure']) > 1200:
            continue
        if weatherData[timestamp.key]['winddirection'] == "":
            continue
        if weatherData[timestamp.key]['windspeed'] == "":
            continue
        if weatherData[timestamp.key]['rain'] == "":
            continue
        try:
            float(weatherData[timestamp.key]['humidity'])
        except:
            continue
        
        for rectangle in rectangles:
            output.write(rectangle.ID)
            output.write(",")
            output.write(timestamp.key)
            
            if binned == False:
            
                output.write(",")
                output.write(weatherData[timestamp.key]['winddirection'])
                output.write(",")
                output.write(weatherData[timestamp.key]['windspeed'])
                output.write(",")
                output.write(weatherData[timestamp.key]['temperature'])
                output.write(",")
                output.write(weatherData[timestamp.key]['humidity'])
                output.write(",")
                output.write(weatherData[timestamp.key]['rain'])
                output.write(",")
                output.write(weatherData[timestamp.key]['pressure'])
                output.write("\n")
            else:
                # winddirection (30 degrees -> 12 variables)
                category = int(float(weatherData[timestamp.key]['winddirection']) / 30.0)
                for i in range(0, 12):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # windspeed (5 m/s bins -> 8 variables)
                category = int(float(weatherData[timestamp.key]['windspeed']) / 5.0)
                for i in range(0, 8):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # temperature (6 celsius degrees -> 6 variables)
                category = int(float(weatherData[timestamp.key]['temperature']) / 5.0)
                for i in range(0, 6):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # humidity
                category = int(float(weatherData[timestamp.key]['humidity']) / 10.0)
                for i in range(0, 10):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # rain
                category = int(weatherData[timestamp.key]['rain'])
                for i in range(0, 2):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # pressure
                category = int((float(weatherData[timestamp.key]['pressure']) - 955.0) / 10.0)
                for i in range(0, 8):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                output.write("\n")
    
    output.close()
    
def appendForecastData(timestamps, inputFile, rectangleFile, outputFile, printPrefixString = ""):

    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, rectangleFile, printPrefixString)    
    
    weatherData = {}
    
    with open(inputFile, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    
    forecastData = data['hourly_forecast']
    
    for forecast in forecastData:
        
        hour = str(forecast["FCTTIME"]["hour_padded"])
        day = str(forecast["FCTTIME"]["mday_padded"])
        month = str(forecast["FCTTIME"]["mon_padded"])
        year = str(forecast["FCTTIME"]["year"])
        timestampKey = year + month + day + hour
                    
        winddirection = str(forecast["wdir"]["degrees"])
        windspeed = str(forecast["wspd"]["metric"])
        temperature = str(forecast["temp"]["metric"])
        rainQpf = float(forecast["qpf"]["metric"])
        humidity = str(float(forecast["humidity"]) / 100.0)
        
        if rainQpf > 0.0:
            rain = "1"
        else:
            rain = "0"
        pressure = str(forecast["mslp"]["metric"])
        
#         print("ts(" + timestampKey + "):wd:" + str(winddirection) + ",ws:" + str(windspeed) + ",t:" + str(temperature) + ",r:" + str(rain) + ",p:" + str(pressure))        
        
        weatherData[timestampKey] = {}
        weatherData[timestampKey]['winddirection'] = winddirection
        weatherData[timestampKey]['windspeed'] = windspeed
        weatherData[timestampKey]['temperature'] = temperature
        weatherData[timestampKey]['rain'] = rain
        weatherData[timestampKey]['pressure'] = pressure
        weatherData[timestampKey]['humidity'] = humidity
        
    output = open(outputFile, 'a')
    
    for timestamp in timestamps:
        if timestamp.key not in weatherData:
            continue
        if weatherData[timestamp.key]['pressure'] == "":
            continue
        if float(weatherData[timestamp.key]['pressure']) < 800 or float(weatherData[timestamp.key]['pressure']) > 1200:
            continue
        if weatherData[timestamp.key]['winddirection'] == "":
            continue
        if weatherData[timestamp.key]['windspeed'] == "":
            continue
        if weatherData[timestamp.key]['rain'] == "":
            continue
        if weatherData[timestamp.key]['humidity'] == "":
            continue
        
        for rectangle in rectangles:
            output.write(rectangle.ID)
            output.write(",")
            output.write(timestamp.key)
            output.write(",")
            output.write(weatherData[timestamp.key]['winddirection'])
            output.write(",")
            output.write(weatherData[timestamp.key]['windspeed'])
            output.write(",")
            output.write(weatherData[timestamp.key]['temperature'])
            output.write(",")
            output.write(weatherData[timestamp.key]['humidity'])
            output.write(",")
            output.write(weatherData[timestamp.key]['rain'])
            output.write(",")
            output.write(weatherData[timestamp.key]['pressure'])
            output.write("\n")
        
    output.close()

def downloadWUDataForStations(apiKeys, stationFile, dates, outputDirectory, printPrefixString = ""):
    stations = []
    
    print(printPrefixString + "Loading " + stationFile + " station file...")
    
    firstLine = True
    # open the file
    with open(stationFile) as infile:
        # read line by line
        for line in infile:
            # skip the first line (header line)
            if firstLine == True:
                firstLine = False
                continue
            # remove newline character from the end
            line = line.rstrip()
            # split the line
            splittedLine = line.split(',')
            station = Station(splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3])
            stations.append(station)
            
    print(printPrefixString + "#stations: " + str(len(stations)))
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Download wu data...")
    for station in stations:
        downloadWeatherDataFromWundergroundWithCoordinates(
            apiKeys, 
            station.latitude, 
            station.longitude, 
            dates, 
            outputDirectory + str(station.ID) + "_" , 
            7.0 / len(apiKeys), 
            "\t\t")
    print(printPrefixString + "Done...")

def processWUDataLocation(inputDirectory, outputFile, printPrefixString = "", fileList = None, binned=False):
        
    weatherData = {}
    
    if fileList == None:
        fileNames = next(os.walk(inputDirectory))[2]
    else:
        fileNames = fileList
        
    for fileName in fileNames:
        
        location = int(fileName[0:fileName.index("_")])
        
        if location not in weatherData:
            weatherData[location] = {}
        
        absoluteFileName = inputDirectory + fileName
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
            
            wData = {}
            wData['winddirection'] = winddirection
            wData['windspeed'] = windspeed
            wData['temperature'] = temperature
            wData['rain'] = rain
            wData['pressure'] = pressure
            wData['humidity'] = humidity
            
            weatherData[location][timestampKey] = wData
                
    output = open(outputFile, 'w')
    if binned==False:
        output.write("location,timestamp,winddirection,windspeed,temperature,humidity,rain,pressure\n")
    else:
        output.write("location,timestamp,")
        for i in range(0, 12):
            output.write("winddirection" + str(i) + ",")
        for i in range(0, 8):
            output.write("windspeed" + str(i) + ",")
        for i in range(0, 6):
            output.write("temperature" + str(i) + ",")
        for i in range(0, 10):
            output.write("humidity" + str(i) + ",")
        for i in range(0,2):
            output.write("rain" + str(i) + ",")
        output.write("pressure0")
        for i in range(1, 8):
            output.write(",pressure" + str(i))
        output.write("\n")
        
    for location in weatherData:
        wData = weatherData[location]
        
        for timestamp in wData:
            data = wData[timestamp]
    
            if data['pressure'] == "":
                continue
            if data['humidity'] == "":
                continue
            if float(data['pressure']) < 800 or float(data['pressure']) > 1200:
                continue
            if data['winddirection'] == "":
                continue
            if data['windspeed'] == "":
                continue
            if data['rain'] == "":
                continue
            try:
                float(data['humidity'])
            except:
                continue
        
            output.write(str(float(location)))
            output.write(",")
            output.write(timestamp)
            
            if binned == False:
            
                output.write(",")
                output.write(data['winddirection'])
                output.write(",")
                output.write(data['windspeed'])
                output.write(",")
                output.write(data['temperature'])
                output.write(",")
                output.write(data['humidity'])
                output.write(",")
                output.write(data['rain'])
                output.write(",")
                output.write(data['pressure'])
                output.write("\n")
            else:
                # winddirection (30 degrees -> 12 variables)
                category = int(float(data['winddirection']) / 30.0)
                for i in range(0, 12):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # windspeed (5 m/s bins -> 8 variables)
                category = int(float(data['windspeed']) / 5.0)
                for i in range(0, 8):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # temperature (6 celsius degrees -> 6 variables)
                category = int(float(data['temperature']) / 5.0)
                for i in range(0, 6):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # humidity
                category = int(float(data['humidity']) / 10.0)
                for i in range(0, 10):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # rain
                category = int(data['rain'])
                for i in range(0, 2):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                # pressure
                category = int((float(data['pressure']) - 955.0) / 10.0)
                for i in range(0, 8):
                    if i == category:
                        output.write(",1")
                    else:
                        output.write(",0")
                output.write("\n")
    
    output.close()
