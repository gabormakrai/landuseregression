import matplotlib.pyplot as plt

def plot(Y, Y_pred, output_filename, Y_label, Y_pred_label):
    index = []
    for i in range(0, len(Y)):
        index.append(i)
        
    fig = plt.figure(figsize=(5.76, 5.76))
    ax = fig.add_subplot(111)
    
    ax.plot(index, Y, '-', label=Y_label)
    ax.plot(index, Y_pred, '-', label=Y_pred_label)
    
    plt.xticks(index, index)
     
    plt.ylabel(r'Pollution concentration levels ($\mu$gm${}^{-3}$)')
    plt.xlabel(r'Hours of the day')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       mode="expand", borderaxespad=0.)

    plt.margins(0.04, 0.04)
    plt.savefig(output_filename)

def plot2(Y, Y_pred, output_filename, Y_label, Y_pred_label):
    index = [i * 10 for i in range(0, len(Y))]
    index2 = [i for i in range(0, len(Y_pred))]
    
    fig = plt.figure(figsize=(5.76, 5.76))
    ax = fig.add_subplot(111)
    
    ax.plot(index, Y, '-', label=Y_label)
    ax.plot(index2, Y_pred, '-', label=Y_pred_label)
    
    plt.xticks(index, [i / 10 for i in index])
    
    plt.ylabel(r'Pollution concentration levels ($\mu$gm${}^{-3}$)')
    plt.xlabel(r'Hours of the day')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       mode="expand", borderaxespad=0.)
    plt.margins(0.04, 0.04)
    plt.savefig(output_filename)
    
def plot3(Y, output_filename, Y_label):
    index = []
    for i in range(0, len(Y)):
        index.append(i)
        
    fig = plt.figure(figsize=(5.76, 5.76))
    ax = fig.add_subplot(111)
    
    ax.plot(index, Y, '-', label=Y_label)
    
    plt.xticks(index, index)
     
    plt.ylabel(r'Pollution concentration levels ($\mu$gm${}^{-3}$)')
    plt.xlabel(r'Hours of the day')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       mode="expand", borderaxespad=0.)

    plt.margins(0.04, 0.04)
    plt.savefig(output_filename)
    