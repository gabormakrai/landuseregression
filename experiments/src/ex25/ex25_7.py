from ex25.ex25_lib import loadX, loadSingleColumnsFile, generateAllDataGroups,\
    getTagAndFeatures

INPUT_DIRECTORY = "/experiments/ex25/"
OUTPUT_FILE = "/experiments/ex25/data.csv"
all_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc', 'lane_length', 'length', 'landuse_area', 'leisure_area', 'buildings_area', 'buildings_number']

all_predictions = []
all_tags = []
for dataGroup in generateAllDataGroups():
    tag, _ = getTagAndFeatures(dataGroup)
    all_predictions.append("pred_" + tag)
    all_tags.append(tag)

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

combined = []

for location in locations:
    testX = loadX(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testX.csv", all_features)
    testY = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testY.csv")
    
    testPreds = []
    
    for tag in all_tags:
        testPred = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testPred_" + tag + ".csv")
        testPreds.append(testPred)

    for i in range(0, len(testY)):
        dataRow = [location, testY[i]]
        for j in range(0, len(testX[i])):
            dataRow.append(testX[i][j])
        for j in range(0, len(testPreds)):
            dataRow.append(testPreds[j][i])
        combined.append(dataRow)

output = open(OUTPUT_FILE, "w")
output.write("location,target")
for f in all_features:
    output.write("," + f)
for p in all_predictions:
    output.write("," + p)
output.write("\n")

for i in range(0, len(combined)):
    for j in range(0, len(combined[i])):
        if j > 0:
            output.write(",")
        output.write(str(combined[i][j]))
    output.write("\n")
    
output.close()
        
