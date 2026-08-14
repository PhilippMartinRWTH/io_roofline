#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math


colors = ['#003a7d', '#d83034', '#ff9d3a', '#4ecb8d', '#ff73b6', 'black']
markers = ['x','+','3','4','.',',']

format = 'png'

aggregate = pd.read_csv('aggregate.csv')

fulldata = pd.read_csv('fulldata.csv')
fulldata['bandwidth'] = fulldata['bytes'] * fulldata['read_mean_rate']

taskdata = pd.read_csv('taskscale.csv')
taskdata['bandwidth'] = taskdata['bytes'] * taskdata['read_mean_rate']

roof1 = taskdata[(taskdata['fs'] == 'tmp') & (taskdata['n_tasks'] == 1) & (taskdata['n_nodes'] == 1) & (taskdata['cluster'] == 'claix23')]
roof4 = taskdata[(taskdata['fs'] == 'tmp') & (taskdata['n_tasks'] == 4) & (taskdata['n_nodes'] == 1) & (taskdata['cluster'] == 'claix23')]
roof48 = taskdata[(taskdata['fs'] == 'tmp') & (taskdata['n_tasks'] == 48) & (taskdata['n_nodes'] == 1) & (taskdata['cluster'] == 'claix23')]
roof96 = taskdata[(taskdata['fs'] == 'tmp') & (taskdata['n_tasks'] == 96) & (taskdata['n_nodes'] == 1) & (taskdata['cluster'] == 'claix23')]

print("tasks: {}, bw: {}, md: {}".format(1, roof1['bandwidth'].max(), roof1['read_mean_rate'].max()))
print("tasks: {}, bw: {}, md: {}".format(4, roof4['bandwidth'].max(), roof4['read_mean_rate'].max()))
print("tasks: {}, bw: {}, md: {}".format(48, roof48['bandwidth'].max(), roof48['read_mean_rate'].max()))
print("tasks: {}, bw: {}, md: {}".format(96, roof96['bandwidth'].max(), roof96['read_mean_rate'].max()))

xlabel = 'Data Density [Byte/IOP]'
ylabel = 'Bandwidth [Byte/s]'

if format == 'pgf':
    plt.rcParams.update({
        "font.family": "serif",  # use serif/main font for text elements
        "text.usetex": True,     # use inline math for ticks
        "pgf.rcfonts": False,     # don't setup fonts from rc parameters
    })


ax = roof1.plot(x='bytes', y='bandwidth', kind='scatter', color=colors[0], marker=markers[0],label='Roofline 1 Task')
roof4.plot(x='bytes', y='bandwidth', kind='scatter', color=colors[1], marker=markers[1],ax=ax,label="Roofline 4 Tasks")
roof48.plot(x='bytes', y='bandwidth', kind='scatter', color=colors[2], marker=markers[2],ax=ax,label="Roofline 48 Tasks")
roof96.plot(x='bytes', y='bandwidth', kind='scatter', color=colors[3], marker=markers[3],ax=ax,label="Roofline 96 Tasks")

aggregate[(aggregate['fs'] == 'tmp') & (aggregate['code'] == 'snappyhex')].plot(x='length', y='bw', kind='scatter', ax=ax, color=colors[4], marker='X', label='Mesh Generation')
aggregate[(aggregate['fs'] == 'tmp') & (aggregate['code'] == 'simplefoam')].plot(x='length', y='bw', kind='scatter', ax=ax, color=colors[4], marker='P', label='SIMPLE Solver')
aggregate[(aggregate['fs'] == 'tmp') & (aggregate['code'] == 'potentialfoam')].plot(x='length', y='bw', kind='scatter', ax=ax, color=colors[4], marker='>', label='Potential Solver')

plt.xscale('log',base=2)
plt.yscale('log',base=2)
#plt.ylim(bottom=1)
#plt.legend(loc=4)

plt.xlabel(xlabel)
plt.ylabel(ylabel)

#plt.grid(which='both')

plt.savefig('tasks'+'.'+format)
plt.close()
