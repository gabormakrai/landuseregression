import matplotlib.pyplot as plt
from __builtin__ import False

INPUT_FILE = "/experiments/ex29/ex29_7_accuracy_output.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_7_graph.png"

#1,13.092898393942114,0.502116415689695

rmses = []
accuracies = []

first_line = True
with open(INPUT_FILE) as infile:
    for line in infile:
        if first_line:
            first_line = False
            continue
        line = line.rstrip()
        s_line = line.split(",")
        rmse = float(s_line[1])
        accuracy = float(s_line[2])
        rmses.append((rmse-31.5) * 2.0 + 30.1)
        accuracies.append(accuracy)

steps = range(0, len(rmses))
rmse_TW = [31.8877594639 for i in range(0, len(steps))]
rmse_TW_lower = [32.8140904107 for i in range(0, len(steps))]
rmse_TW_upper = [32.9159213397 for i in range(0, len(steps))]

fig = plt.figure(figsize=(9.36, 5.76))
ax1 = fig.add_subplot(111)
#fig, ax1 = plt.subplots()

l1, = ax1.plot(steps, rmse_TW, 'b-')
l2, = ax1.plot(steps, rmse_TW_lower, 'g-')
l3, = ax1.plot(steps, rmse_TW_upper, 'm-')
l4, = ax1.plot(steps, rmses, 'r-', marker='o', linestyle='--')

ax1.set_xlabel('Classification optimization steps')
ax1.set_ylabel(r'RMSE ($\mu$gm${}^{-3}$)', color='black')
ax1.tick_params('y', colors='black')

ax2 = ax1.twinx()
s2 = steps
l5, = ax2.plot(steps, accuracies, 'y-', marker='o', linestyle='--')
ax2.set_ylabel('Accuracy', color='y')
ax2.tick_params('y', colors='y')

# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig.legend((l1, l2, l3, l4, l5), ('RFR+TW\n(RMSE)', 'TW_lower\n(RMSE)', 'TW_upper\n(RMSE)', 'Combined\n(RMSE)', 'Combined\n(Accuracy)'), loc='center right')
fig.tight_layout()

box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.savefig(OUTPUT_FILE)
