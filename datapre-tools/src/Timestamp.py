
DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

class Timestamp:
    """
    This class represents the timestamp for the regression. It only contains
    year,month,day,hour to be able to model hourly averages.
    """
    
    def createBasedOnKey(self, key):
        self.key = key
        self.year = int(key[0:4])
        self.month = int(key[4:6])
        self.day = int(key[6:8])
        self.hour = int(key[8:10])
        return self
        
    def createBasedOnOther(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.key = str(year)
        if month < 10:
            self.key = self.key + "0"
        self.key = self.key + str(month)
        if day < 10:
            self.key = self.key + "0"
        self.key = self.key + str(day)
        if hour < 10:
            self.key = self.key + "0"
        self.key = self.key + str(hour)
        return self
        
    def toString(self):
        return "Timestamp(key:" + self.key + ")"
    
    def __eq__(self, other):
        return self.key == other.key
    
    def __hash__(self):
        return self.key.__hash__()
    def __str__(self):
        return self.toString()

def generateTimestamps(year):
    timestamps = []
    for month in range(1, 13):
        for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
            for hour in range(0, 24):
                t = Timestamp().createBasedOnOther(year, month, day, hour)
                timestamps.append(t)
    return timestamps

def generateTimestampsForMonth(year, month):
    timestamps = []
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
        for hour in range(0, 24):
            t = Timestamp().createBasedOnOther(year, month, day, hour)
            timestamps.append(t)
    return timestamps

def generateTimestampsForDays(year, month, day1, day2):
    timestamps = []
    for day in range(day1, day2 + 1):
        for hour in range(0, 24):
            t = Timestamp().createBasedOnOther(year, month, day, hour)
            timestamps.append(t)
    return timestamps    

def generateDatesStringForYear(year):
    dates = []
    for month in range(1, 13):
        for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
                dateString = str(year)
                if (month < 10):
                    dateString = dateString + "0"
                dateString = dateString + str(month)
                if (day < 10):
                    dateString = dateString + "0"
                dateString = dateString + str(day)
                dates.append(dateString)
    return dates
    
    