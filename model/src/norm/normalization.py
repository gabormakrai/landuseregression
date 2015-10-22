
class Normalization:
    
    def stat(self, data):
        self.min = {}
        self.max = {}
        for column in data:
            minValue = float("inf")
            maxValue = float("-inf")
            
            for i in range(0, len(data[column])):
                if data[column][i] < minValue:
                    minValue = data[column][i]
                if data[column][i] > maxValue:
                    maxValue = data[column][i]
                    
            self.min[column] = minValue
            self.max[column] = maxValue
                
    def normalize(self, data):
        for column in data:
            minValue = self.min[column]
            maxValue = self.max[column]
            for i in range(0, len(data[column])):
                data[column][i] = (data[column][i] - minValue) / (maxValue - minValue)
                
        for column in data:
            minValue = float("inf")
            maxValue = float("-inf")
            
            for i in range(0, len(data[column])):
                if data[column][i] < minValue:
                    minValue = data[column][i]
                if data[column][i] > maxValue:
                    maxValue = data[column][i]
                        
    def denormalize(self, data, targetColumn):
        
        minValue = self.min[targetColumn]
        maxValue = self.max[targetColumn]
        
        for i in range(0, len(data)):
            data[i] = data[i] * (maxValue - minValue) + minValue
        
    def __str__(self):
        return "Normalization"
    