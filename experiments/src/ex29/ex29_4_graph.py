import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE_1 = "/experiments/ex29/ex29_4.csv"
INPUT_FILE_2 = "/experiments/ex29/ex29_4_1.csv"
INPUT_FILE_3 = "/experiments/ex29/ex29_4_2.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_4.png"

data = defaultdict(lambda: defaultdict(lambda: 0.0))

# min_samples_leaf,n_estimators,rmse
def load_data(file_name, data):
    first_line = True
    with open(file_name) as infile:
        for line in infile:
            line = line.rstrip()
            if first_line:
                first_line = False
                continue
            s_line = line.split(',')
            rmse = float(s_line[2])
            min_samples_leaf = int(s_line[0])
            n_estimators = int(s_line[1])
            data[min_samples_leaf][n_estimators] = rmse

load_data(INPUT_FILE_1, data)
load_data(INPUT_FILE_2, data)
load_data(INPUT_FILE_3, data)

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = range(2,100)

colors = []
for i in range(0,51):
    c = hex(20 + 3 * i).split('x')[-1]
    color = "#" + c + c + c
    colors.append(color)

for n in range(50,101):
    data1 = []
    for x1 in x:
        data1.append(data[x1][n])
    if n % 5 == 0:
        ax.plot(x, data1, color=colors[n-50], label="estimator_" + str(n))
    else:
        ax.plot(x, data1, color=colors[n-50])

plt.xlabel("min_leaf")
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.legend()

plt.savefig(OUTPUT_FILE)

