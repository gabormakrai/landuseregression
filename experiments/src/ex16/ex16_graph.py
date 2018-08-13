import matplotlib.pyplot as plt

INPUT_DATA_FILE = "/experiments/ex16/rmse_output.csv"
OUTPUT_FILE = "/experiments/ex16/ex16.png"

def loadData(fileName):
    rmseResult = []
    print("Open file " + fileName + "...")
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:                
            # remove newline character from the end
            line = line.rstrip()
            # split the line
            splittedLine = line.split(';')
            rmseResult.append(float(splittedLine[1]))
    print("Done...")
    return rmseResult
            
data = loadData(INPUT_DATA_FILE)

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)
 
x = [i for i in range(0, len(data))]
ax.plot(x, data)
 
plt.ylim(11.5, 18.0)
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("Feature selection iterations")
 
plt.savefig(OUTPUT_FILE)
plt.close()

all_features = []
all_features.extend(['leisure_area', 'landuse_area'])
all_features.extend(['buildings_number', 'buildings_area'])
all_features.extend(['lane_length', 'length'])
all_features.extend(['atc'])
all_features.extend(['winddirection', 'windspeed', 'temperature', 'rain', 'pressure'])
all_features.extend(['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day'])

global_best_result = 12.613385504601814
global_best_step = [True, False, False, False, False, False, False, False, True, True, True, True, True, True, False, True, False]

print("Best RMSE: " + str(global_best_result))
print("Best Step: " + str(global_best_step))
best_features = [all_features[i] for i in range(0, len(all_features)) if global_best_step[i]]  
print("Best features:" + str(best_features))




