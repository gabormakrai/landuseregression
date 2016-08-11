from Timestamp import generateTimestamps
from rectangles import loadRectangles
from datetime import datetime

def createTimeFile(timestamps, inputRectangleFile, outputFile, printPrefixString = "", binned=False):
         
    bankHolidays = set([
        "20120102", "20120406", "20120409", "20120507", "20120604", "20120605", "20120827", "20121225", "20121226",
        "20130101", "20130329", "20130401", "20130506", "20130527", "20130826", "20131225", "20131226",
        "20140101", "20140418", "20140421", "20140505", "20140526", "20140825", "20141225", "20141226",
        "20150101", "20150403", "20150406", "20150504", "20150525", "20150831", "20151225", "20151228",
        "20160101", "20160325", "20160328", "20160502", "20160530", "20160829", "20161226", "20161227"
    ])
    
    raceDays = set([
        "20120516", "20120517", "20120518", "20120526", "20120615", "20120616",
        "20120713", "20120714", "20120727", "20120728", "20120822", "20120823",
        "20120824", "20120825", "20120909", "20121012", "20121013", "20130515",
        "20130516", "20130517", "20130523", "20130614", "20130615", "20130712",
        "20130713", "20130726", "20130727", "20130821", "20130822", "20130823",
        "20130824", "20130908", "20131011", "20131012", "20140514", "20140515",
        "20140516", "20140531", "20140613", "20140614", "20140711", "20140712",
        "20140725", "20140726", "20140820", "20140821", "20140822", "20140823",
        "20140907", "20141010", "20141011", "20150513", "20150514", "20150515",
        "20150530", "20150612", "20150613", "20150710", "20150711", "20150724",
        "20150725", "20150819", "20150820", "20150821", "20150822", "20150906",
        "20151009", "20151010", "20160511", "20160512", "20160513", "20160521",
        "20160610", "20160611", "20160708", "20160709", "20160722", "20160723",
        "20160817", "20160818", "20160819", "20160820", "20160904", "20161007",
        "20161008" 
    ])
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)

    print(printPrefixString + "Writing out time related data to " + outputFile)
    
    output = open(outputFile, 'w')
    if binned==False:
        output.write("location,timestamp,hour,day_of_week,month,bank_holiday,race_day\n")
    else:
        output.write("location,timestamp")
        for i in range(0, 24):
            output.write(",hour" + str(i))
        for i in range(0, 7):
            output.write(",day_of_week" + str(i))
        for i in range(0, 12):
            output.write(",month" + str(i))
        output.write(",bank_holiday,race_day\n")
    
    for rectangle in rectangles:
        for timestamp in timestamps:
            hour = str(timestamp.hour)
            month = str(timestamp.month)
            
            d = datetime(timestamp.year, timestamp.month, timestamp.day)
            dayOfWeek = str(d.weekday())
            
            timestampDay = timestamp.key[0:8]
            
            bankHoliday = "0"
            if timestampDay in bankHolidays:
                bankHoliday = "1"
                
            raceDay = "0"
            if timestampDay in raceDays:
                raceDay = "1"

            if binned==False:                
                output.write(str(rectangle.ID) + "," + timestamp.key + "," + hour + "," + dayOfWeek + "," + month + "," + bankHoliday + "," + raceDay + "\n")
            else:
                output.write(str(rectangle.ID) + "," + timestamp.key + ",")
                # hour
                for i in range(0, 24):
                    if str(i) == hour: output.write("1")
                    else: output.write("0")
                    output.write(",")
                # dayOfWeek
                for i in range(0, 7):
                    if str(i) == dayOfWeek: output.write("1")
                    else: output.write("0")
                    output.write(",")
                # month
                for i in range(1, 13):
                    if str(i) == month: output.write("1")
                    else: output.write("0")
                    output.write(",")
                
                output.write(bankHoliday + "," + raceDay + "\n")                
            
    output.close()
    
    print(printPrefixString + "Done...")
    
def createTimeFileBinned(inputRectangleFile, outputFile, printPrefixString = ""):
    
    timestamps = generateTimestamps(2013)
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)

    print(printPrefixString + "Writing out time related data to " + outputFile)
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,")
    for i in range(0, 24):
        output.write("hour" + str(i) + ",")
    for i in range(0, 7):
        output.write("day_of_week" + str(i) + ",")
    for i in range(0, 12):
        output.write("month" + str(i) + ",")
    output.write("bank_holiday,race_day\n")
    
    for rectangle in rectangles:
        for timestamp in timestamps:
            hour = int(str(timestamp.hour))
            d = datetime(timestamp.year, timestamp.month, timestamp.day)
            dayOfWeek = int(str(d.weekday()))
            month = int(str(timestamp.month))
            bankHoliday = "0"
            # 01/01/2013, 29/03/2013, 01/04/2013, 06/05/2013, 27/05/2013, 26/08/2013, 25/12/2015, 26/12/2015
            monthday = timestamp.key[4:8]
            if monthday == "0101" or monthday == "0329" or monthday == "0401" or monthday == "0506" or monthday == "0527" or monthday == "0826" or monthday == "1225" or monthday == "1226":
                bankHoliday = "1"
                
            raceDays = set([ "0515", "0516", "0517", "0525", "0614", "0615", "0712", "0713", "0726", "0727", "0821", "0822", "0823", "0824", "0908", "1011", "1012" ])
            raceDay = "0"
            if monthday in raceDays:
                raceDay = "1"
    
            output.write(str(rectangle.ID) + "," + timestamp.key + ",")
            # hour
            for i in range(0, 24):
                if i == hour: output.write("1")
                else: output.write("0")
                output.write(",")
            # dayOfWeek
            for i in range(0, 7):
                if i == dayOfWeek: output.write("1")
                else: output.write("0")
                output.write(",")
            # month
            for i in range(0, 12):
                if i == month: output.write("1")
                else: output.write("0")
                output.write(",")
            
            output.write(bankHoliday + "," + raceDay + "\n")
    output.close()
    
    print(printPrefixString + "Done...")