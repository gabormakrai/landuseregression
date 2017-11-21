import matplotlib.pyplot as plt

OUTPUT_FILE = "/experiments/ex28/ex28_4.png"
data = [
    [0,12.8585060253184,13.64639145046649,13.142224500967206,0.5216387470819117],
    [1,12.8585060253184,13.64639145046649,13.0775250785714,0.5223570457402325],
    [2,12.8585060253184,13.64639145046649,12.966768239170207,0.5372617429003874],
    [3,12.8585060253184,13.64639145046649,12.933272580543633,0.5418280700854262],
    [4,12.8585060253184,13.64639145046649,12.918273879081715,0.5448808393832892],
    [5,12.8585060253184,13.64639145046649,12.873261334399082,0.5479849157281753],
    [6,12.8585060253184,13.64639145046649,12.839132201280314,0.550396346938252]
]
steps = [int(v[0]) for v in data]
rmse_TW = [v[1] for v in data]
rmse_TWA = [v[2] for v in data]
rmse_Combined = [v[3] for v in data]
accuracy_Combined = [v[4] for v in data]  

fig, ax1 = plt.subplots()

l1, = ax1.plot(steps, rmse_TW, 'b-')
l2, = ax1.plot(steps, rmse_TWA, 'g-')
l3, = ax1.plot(steps, rmse_Combined, 'r-')

ax1.set_xlabel('Classification optimization steps')
ax1.set_ylabel('RMSE', color='black')
ax1.tick_params('y', colors='black')

ax2 = ax1.twinx()
s2 = steps
l4, = ax2.plot(steps, accuracy_Combined, 'y-')
ax2.set_ylabel('Accuracy', color='y')
ax2.tick_params('y', colors='y')

# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig.legend((l1, l2, l3, l4), ('RFR+TW\n(RMSE)', 'RFR+TWA\n(RMSE)', 'Combined\n(RMSE)', 'Combined\n(Accuracy)'), loc='center right')
fig.tight_layout()

box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.75, box.height])
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.75, box.height])

plt.savefig(OUTPUT_FILE)
