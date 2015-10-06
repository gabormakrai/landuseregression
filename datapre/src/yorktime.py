from Timestamp import generateTimestamps
from rectangles import loadRectangles
from datetime import datetime

def createTimeFile(inputRectangleFile, outputFile, printPrefixString = ""):
    
    timestamps = generateTimestamps(2013)
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)

    print(printPrefixString + "Writing out time related data to " + outputFile)
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,hour,day_of_week,month,bank_holiday,race_day\n")
    
    for rectangle in rectangles:
        for timestamp in timestamps:
            hour = str(timestamp.hour)
            d = datetime(timestamp.year, timestamp.month, timestamp.day)
            dayOfWeek = str(d.weekday())
            month = str(timestamp.month)
            bankHoliday = "0"
            # 01/01/2013, 29/03/2013, 01/04/2013, 06/05/2013, 27/05/2013, 26/08/2013, 25/12/2015, 26/12/2015
            monthday = timestamp.key[4:8]
            if monthday == "0101" or monthday == "0329" or monthday == "0401" or monthday == "0506" or monthday == "0527" or monthday == "0826" or monthday == "1225" or monthday == "1226":
                bankHoliday = "1"
                
            raceDays = set([ "0515", "0516", "0517", "0525", "0614", "0615", "0712", "0713", "0726", "0727", "0821", "0822", "0823", "0824", "0908", "1011", "1012" ])
            raceDay = "0"
            if monthday in raceDays:
                raceDay = "1"
    
            output.write(str(rectangle.ID) + "," + timestamp.key + "," + hour + "," + dayOfWeek + "," + month + "," + bankHoliday + "," + raceDay + "\n")
    output.close()
    
    print(printPrefixString + "Done...")
    