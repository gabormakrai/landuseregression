import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_knn1.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_knn1_uniform.png"
OUTPUT_FILE_2 = "/experiments/ex1/ex1_knn1_distance.png"

data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        if firstLine:
            firstLine = False
            continue
        s_line = line.split(',')
        method = s_line[0]
        p = int(float(s_line[1]))
        neighbours = int(s_line[2])
        rmse = float(s_line[3])
        data[method][p][neighbours] = rmse

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)
 
names = []
dataToPlot = []
 
x = range(2, 100)

for p in [1, 2, 3, 4]:
    names.append("p_" + str(p))
    d = []
    for x1 in x:
        d.append(data['uniform'][p][x1])
    dataToPlot.append(d)
   
for i in range(0, len(names)):
    ax.plot(x, dataToPlot[i], label=names[i])
 
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("neighbours")
plt.legend()
 
plt.savefig(OUTPUT_FILE_1)

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)
 
names = []
dataToPlot = []
 
x = range(2, 100)

for p in [1, 2, 3, 4]:
    names.append("p_" + str(p))
    d = []
    for x1 in x:
        d.append(data['distance'][p][x1])
    dataToPlot.append(d)
   
for i in range(0, len(names)):
    ax.plot(x, dataToPlot[i], label=names[i])
 
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("neighbours")
plt.legend()
 
plt.savefig(OUTPUT_FILE_2)
