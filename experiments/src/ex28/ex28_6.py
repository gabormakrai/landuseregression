import matplotlib.pyplot as plt

OUTPUT_FILE = "/experiments/ex28/ex28_6.png"
#step,rmse_tw,rmse_lower,rmse_upper,rmse_combined,accuracy
data = [    
[0,27.48993891627752,32.778350765112144,33.47066117432977,27.60257615802804,0.6736845936656666],
[1,27.48993891627752,32.778350765112144,33.47066117432977,27.23570265566812,0.691249343531773],
[2,27.48993891627752,32.778350765112144,33.47066117432977,26.244605974667767,0.7372203185365829],
[3,27.48993891627752,32.778350765112144,33.47066117432977,26.613570103006236,0.714351825371652],
[4,27.48993891627752,32.778350765112144,33.47066117432977,26.423377466289665,0.7742685254033704],
[5,27.48993891627752,32.778350765112144,33.47066117432977,25.879612315059497,0.8019727845172294],
[6,27.48993891627752,32.778350765112144,33.47066117432977,25.865266336406204,0.8037926964334926]   
]

steps = [int(v[0]) for v in data]
rmse_TW = [v[1] for v in data]
rmse_TW_lower = [v[2] for v in data]
rmse_TW_upper = [v[3] for v in data]
rmse_TW_combined = [v[4] for v in data]
accuracy_combined = [v[5] for v in data]  

fig, ax1 = plt.subplots()

l1, = ax1.plot(steps, rmse_TW, 'b-')
l2, = ax1.plot(steps, rmse_TW_lower, 'g-')
l3, = ax1.plot(steps, rmse_TW_upper, 'r-')
l4, = ax1.plot(steps, rmse_TW_combined, 'm-')

ax1.set_xlabel('Classification optimization steps')
ax1.set_ylabel('RMSE', color='black')
ax1.tick_params('y', colors='black')

ax2 = ax1.twinx()
s2 = steps
l5, = ax2.plot(steps, accuracy_combined, 'y-')
ax2.set_ylabel('Accuracy', color='y')
ax2.tick_params('y', colors='y')

# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig.legend((l1, l2, l3, l4, l5), ('RFR+TW\n(RMSE)', 'RFR+TW lower\n(RMSE)', 'RFR+TW upper\n(RMSE)', 'Combined\n(RMSE)', 'Combined\n(Accuracy)'), loc='center right')
fig.tight_layout()

box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.65, box.height])
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.65, box.height])

plt.savefig(OUTPUT_FILE)
