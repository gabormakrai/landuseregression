from data.data import loadData
from copy import deepcopy
from ex18_lib import doPrediction

#DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
DATA_FILE = "/media/sf_lur/data/" + "data3_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex18/"

#locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
locations = [2.0, 3.0, 4.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

# all
features = deepcopy(columns)
features.remove('location')
features.remove('timestamp')
features.remove('target')
columns2 = deepcopy(features)
columns2.extend(['location', 'timestamp', 'target', 'prediction'])

doPrediction(locations, data, columns, features, columns2, OUTPUT_DIRECTORY + "all.csv")

# t+w
features = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day']
columns2 = deepcopy(features)
columns2.extend(['location', 'timestamp', 'target', 'prediction'])

doPrediction(locations, data, columns, features, columns2, OUTPUT_DIRECTORY + "tw.csv")

# t+w+a
features = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'atc']
columns2 = deepcopy(features)
columns2.extend(['location', 'timestamp', 'target', 'prediction'])

doPrediction(locations, data, columns, features, columns2, OUTPUT_DIRECTORY + "twa.csv")

# w+a
# t+w+a
features = ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc']
columns2 = deepcopy(features)
columns2.extend(['location', 'timestamp', 'target', 'prediction'])

doPrediction(locations, data, columns, features, columns2, OUTPUT_DIRECTORY + "wa.csv")
