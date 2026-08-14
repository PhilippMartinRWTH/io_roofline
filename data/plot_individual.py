#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math

data = pd.read_csv('imagenet_tmp.csv')

colors = ['#003a7d', '#d83034', '#ff9d3a', '#4ecb8d', '#ff73b6', 'black']
markers = ['x','+','3','4','.',',']

print(data)

format = 'png'


data['time'] = data['end_time'] - data['start_time']
data['bandwidth'] = data['length'] / data['time']

xlabel = 'Data Density [Byte/IOP]'
ylabel = 'Bandwidth [Byte/s]'

if format == 'pgf':
    plt.rcParams.update({
        "font.family": "serif",  # use serif/main font for text elements
        "text.usetex": True,     # use inline math for ticks
        "pgf.rcfonts": False,     # don't setup fonts from rc parameters
    })


ax = data.plot(x='length', y='bandwidth', kind='scatter', color=colors[0], marker=markers[0])

plt.xscale('log',base=2)
plt.yscale('log',base=2)
#plt.ylim(bottom=1)
#plt.legend(loc=4)

plt.xlabel(xlabel)
plt.ylabel(ylabel)

#plt.grid(which='both')

plt.savefig('individual_operations'+'.'+format)
plt.close()