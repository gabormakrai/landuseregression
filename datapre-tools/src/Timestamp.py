
DAYS_OF_MONTH = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

class Timestamp:
    """
    This class represents the timestamp for the regression. It only contains
    year,month,day,hour to be able to model hourly averages.
    """
    
    def createBasedOnKey(self, key):
        self.key = key
        self.year = int(key[0:3])
        self.month = int(key[4:5])
        self.day = int(key[6:7])
        self.hour = int(key[8:9])
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

