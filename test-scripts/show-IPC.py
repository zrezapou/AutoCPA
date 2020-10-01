import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
def read_csv(addr):
    return pd.read_csv(addr, index_col=False)

def plot_stats(labels, stats, inst):
    font = {'family' : 'Helvetica',
        # 'weight' : 'bold',
        'size'   : 18}

    matplotlib.rc('font', **font)
    lst=[]
    x_pos=np.arange(0,2)
    plt.figure(figsize=(18, 9),)
    avg, std=[], []
    for i in range(2):
        avg.append(stats[i].loc["avg"][inst])
        std.append(stats[i].loc["std"][inst])
    plt.bar(x_pos, avg, yerr=std, align='center', alpha=0.5, ecolor='black', capsize=10, width=0.5)
    plt.ylabel("Instructions Per Cycle")
    plt.xticks(x_pos, labels)
    plt.title(inst)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('./results/result-'+inst+'.png')
    

files=["redis-original.csv", "redis-reorder.csv"]
labels=["Original", "Re-ordered"]
df=[read_csv(file) for file in files]
for i in range(2):
    df[i]=df[i].set_index("Unnamed: 0")
columns=df[0].columns.values
for col in columns:
    plot_stats(labels, df, col)
