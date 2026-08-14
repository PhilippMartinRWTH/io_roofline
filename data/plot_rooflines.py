#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math


colors = ['#003a7d', '#d83034', '#ff9d3a', '#4ecb8d', '#ff73b6', 'black']
markers = ['x','+','3','4','.',',']

format = 'pgf'

aggregate = pd.read_csv('aggregate.csv')

fulldata = pd.read_csv('fulldata.csv')
fulldata['bandwidth'] = fulldata['bytes'] * fulldata['read_mean_rate']

taskdata = pd.read_csv('taskscale.csv')
taskdata['bandwidth'] = taskdata['bytes'] * taskdata['read_mean_rate']

#roof_tmp = fulldata[(fulldata['fs'] == 'tmp') & (fulldata['n_tasks'] == 50) & (fulldata['n_nodes'] == 1) & (fulldata['cluster'] == 'claix23')]
roof_tmp = taskdata[(taskdata['fs'] == 'tmp') & (taskdata['n_tasks'] == 4) & (taskdata['n_nodes'] == 1) & (taskdata['cluster'] == 'claix23')]
roof_beeond = fulldata[(fulldata['fs'] == 'beeond') & (fulldata['n_tasks'] == 4) & (fulldata['n_nodes'] == 1) & (fulldata['cluster'] == 'claix23')]

xlabel = 'Data Density [Byte/IOP]'
ylabel = 'Bandwidth [Byte/s]'

if format == 'pgf':
    plt.rcParams.update({
        "font.family": "serif",  # use serif/main font for text elements
        "text.usetex": True,     # use inline math for ticks
        "pgf.rcfonts": False,     # don't setup fonts from rc parameters
    })


ax = roof_tmp.plot(x='bytes', y='bandwidth', kind='scatter', color=colors[0], marker=markers[0],label='Roofline local')
roof_beeond.plot(x='bytes', y='bandwidth', kind='scatter', color=colors[1], marker=markers[1],ax=ax,label="Roofline parallel")

aggregate[(aggregate['fs'] == 'tmp') & (aggregate['code'] == 'imagenet')].plot(x='length', y='bw', kind='scatter', ax=ax, color=colors[2], marker='X', label='ImageNet local')
aggregate[(aggregate['fs'] == 'lustre') & (aggregate['code'] == 'imagenet')].plot(x='length', y='bw', kind='scatter', ax=ax, color=colors[2], marker='P', label='ImageNet parallel')
aggregate[(aggregate['fs'] == 'lustre') & (aggregate['code'] == 'cifar1')].plot(x='length', y='bw', kind='scatter', ax=ax, color=colors[3], marker='X', label='CIFAR-100 phase 1')
aggregate[(aggregate['fs'] == 'lustre') & (aggregate['code'] == 'cifar2')].plot(x='length', y='bw', kind='scatter', ax=ax, color=colors[4], marker='X', label='CIFAR-100 phase 2')

plt.xscale('log',base=2)
plt.yscale('log',base=2)
#plt.ylim(bottom=1)
#plt.legend(loc=4)

plt.xlabel(xlabel)
plt.ylabel(ylabel)

#plt.grid(which='both')

plt.savefig('rooflines'+'.'+format)
plt.close()
