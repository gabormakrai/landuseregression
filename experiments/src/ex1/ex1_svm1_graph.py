import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_svm1.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_svm1.png"

# data: n_estimators,C,max_samples
data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        if firstLine:
            firstLine = False
            continue
        line = line.rstrip()
        s_line = line.split(',')
        n_estimators = int(s_line[0])
        c = int(s_line[1])
        max_samples = int(s_line[2])
        data[n_estimators][c][max_samples] = float(s_line[3])

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)
 
names = []
dataToPlot = []
 
x = range(5,15)

for c in [100]: #, 300, 600, 1000, 1200, 1500, 2000, 3000]:
    for samples in [1000, 2000, 3000, 4000, 5000]:
        names.append("samples_" + str(samples) +",c_" + str(c))
        d = []
        for x1 in x:
            d.append(data[x1][c][samples])
        dataToPlot.append(d)
   
for i in range(0, len(names)):
    ax.plot(x, dataToPlot[i], label=names[i])
 
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("Estimators")
 
plt.savefig(OUTPUT_FILE_1)
