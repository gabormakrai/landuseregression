def generateTimestampWeek():
    DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
    
    week = 0
    weekoftheday = 1
    
    weekCategory = {}
        
    for month in range(1, 13):
        for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
            weekoftheday = weekoftheday + 1
            if weekoftheday == 8:
                weekoftheday = 1
                week = week + 1
            week2 = week
            if week < 1:
                week2 = 1
            elif week > 51:
                week = 51
            
            if day < 10:
                dayString = "0" + str(day)
            else:
                dayString = str(day) 
    
            if month < 10:
                monthString = "0" + str(month)
            else:
                monthString = str(month)
            
            for hour in range(0, 24):
                if hour < 10:
                    hourString = "0" + str(hour)
                else:
                    hourString = str(hour)
            
                timestamp = "2013" + monthString + dayString + hourString
                
                weekCategory[timestamp] = week2
    
    return weekCategory