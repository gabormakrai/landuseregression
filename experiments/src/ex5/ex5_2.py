from sklearn import decomposition
from data.data import loadData
from sklearn import preprocessing

OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex5/"

data = {}
columns = []
loadData(OUTPUT_DIRECTORY + "errors_rae.csv", [], data, columns)

targetColumn = "error_rae"

trainColumns = []
for column in columns:
    if column != targetColumn:
        trainColumns.append(column)
        
trainData = []

for i in range(0, len(data[targetColumn])):
    record = []
    for column in trainColumns:
        record.append(data[column][i])
    trainData.append(record)

print(str(trainColumns))
print(str(len(trainColumns)))

trainDataScaled = preprocessing.scale(trainData)

pca = decomposition.PCA(n_components=20)

pca.fit(trainDataScaled, data[targetColumn])

print(str(pca.explained_variance_))

