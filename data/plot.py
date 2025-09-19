#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math

data = pd.read_csv('filesystems.csv')

#bandwidth [byte/s]
data['bw_write'] = (data['bytes'] * data['write_mean_rate'])
data['bw_read'] = (data['bytes'] * data['read_mean_rate']) 

data['bw_write_sd'] = (data['bytes'] * data['write_sd_rate'])
data['bw_read_sd'] = (data['bytes'] * data['read_sd_rate']) 

#densities [byte/IOPS]
data['density_write'] = data['bytes']
data['density_read'] = data['bytes']

#intensities [IOPS/byte]
data['intensity_write'] = 1 / data['bytes']
data['intensity_read'] = 1 / data['bytes']

colors = ['#003a7d', '#d83034', '#ff9d3a', '#4ecb8d', '#ff73b6', 'black']
markers = ['x','+','3','4','.',',']

format = 'pgf'

def plot(name, output, plots):
    ax = None
    count = 0

    xlabel = 'Data Density [Byte/IOP]'
    ylabel = 'Bandwidth [Byte/s]'

    for pl in plots:
        mydata = data.copy()
        operation = 'write'
        label = ''
        for key in pl:
            if key == 'operation':
                operation = pl['operation']
            elif key == 'label':
                label = pl['label']
            else:
                mydata = mydata[(mydata[key] == pl[key])]

        if format == 'pgf':
            plt.rcParams.update({
                "font.family": "serif",  # use serif/main font for text elements
                "text.usetex": True,     # use inline math for ticks
                "pgf.rcfonts": False,     # don't setup fonts from rc parameters
            })

        def mean_of_sd(x):
            res = 0
            for e in x:
                res += e*e
            res /= x.size
            res = math.sqrt(res)
            return res

        mydata = mydata.groupby('bytes').aggregate({
            'density_write':'mean', 
            'intensity_write':'mean', 
            'bw_write':'mean', 
            'bw_write_sd':mean_of_sd,
            'write_mean_rate':'mean', 
            'write_sd_rate':mean_of_sd, 
            'density_read':'mean', 
            'intensity_read':'mean', 
            'bw_read':'mean', 
            'bw_read_sd':mean_of_sd,
            'read_mean_rate':'mean', 
            'read_sd_rate':mean_of_sd, 
            'stat_mean_rate':'mean',
            'stat_sd_rate':mean_of_sd,
            'removal_mean_rate':'mean',
            'removal_sd_rate':mean_of_sd,
            })

        if label == '':
            label = '{}'.format(pl['fs'])

        xax = 'density_'+operation
        yax = 'bw_'+operation
        yerr = 'bw_'+operation+'_sd'

        if operation in ['removal', 'stat']:
            xax = 'intensity_write'
            yax = operation+'_mean_rate'
            yerr = operation+'_sd_rate'
            xlabel = 'Metadata Intensity [IOP/Byte]'
            ylabel = 'Metadata Rate [IOP/s]'

        print("{} with {} and {}".format(operation, xax, yax))

        if not ax:
            ax = mydata.plot(x=xax, y=yax, yerr=yerr, kind='scatter', title=name, legend=True, label=label, color=colors[count], marker=markers[count])
        else:
            mydata.plot(x=xax, y=yax, yerr=yerr, kind='scatter', ax=ax, label=label, color=colors[count], marker=markers[count])

        count = count+1

    if output == 'hyp5':
        foam_data = pd.read_csv('openfoam.csv')
        foam_data['bandwidth'] = foam_data['bandwidth'] * 1024 * 1024
        foam_data['data_density'] = (foam_data['total_bytes'] * 1024 * 1024) / foam_data['write_operations']

        foam_data[foam_data['filesystem'] == 'tmp'].plot(x='data_density',y='bandwidth', kind='scatter', ax=ax, color='#008dff', marker='X', label='OpenFOAM local')
        foam_data[foam_data['filesystem'] == 'beeond'].plot(x='data_density',y='bandwidth', kind='scatter', ax=ax, color='#9d2c00', marker='P', label='OpenFOAM ad-hoc')
        foam_data[foam_data['filesystem'] == 'lustre'].plot(x='data_density',y='bandwidth', kind='scatter', ax=ax, color='#f0c571', marker='<', label='OpenFOAM parallel')

    plt.xscale('log',base=2)
    plt.yscale('log',base=2)
    #plt.ylim(bottom=1)
    plt.legend(loc=4)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(output+'.'+format)
    plt.close()

#MD-BW Comparison

#Hypothesis 1: stat/unlink
plot('Pure Metadata Operations','hyp1',[
    {'cluster':'claix18','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'stat', 'label':'Stat'},
    {'cluster':'claix18','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'removal', 'label':'Unlink'}
    ])

#Hypothesis 2: read/write
plot('Bandwidth Operations','hyp2',[
    {'cluster':'claix23','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'read', 'label':'Read'},
    {'cluster':'claix23','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Write'}
    ])

#Hypothesis 3a: Filesystems
plot('Filesystem Comparison CLUSTER-2','hyp3a',[
    {'cluster':'claix23','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Local'},
    {'cluster':'claix23','fs':'beeond','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Ad-hoc'},
    {'cluster':'claix23','fs':'lustre','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Parallel'}
    ])

plot('Filesystem Comparison CLUSTER-1','hyp3a1',[
    {'cluster':'claix18','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Local'},
    {'cluster':'claix18','fs':'beeond','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Ad-hoc'},
    {'cluster':'claix18','fs':'lustre','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Parallel'}
    ])

#Hypothesis 3b: Node Counts
plot('Node Count Comparison','hyp3b',[
    {'cluster':'claix23','fs':'beeond','n_tasks':4,'n_nodes':4,'n_files':1000,'operation':'write', 'label':'4 Nodes'},
    {'cluster':'claix23','fs':'beeond','n_tasks':4,'n_nodes':2,'n_files':1000,'operation':'write', 'label':'2 Nodes'},
    {'cluster':'claix23','fs':'beeond','n_tasks':4,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'1 Node'},
    ])

#Hypothesis 3c: Task Counts
plot('Task Count Comparison','hyp3c',[
    {'cluster':'claix23','fs':'tmp','n_tasks':50,'n_nodes':1,'operation':'write', 'label':'50 Tasks'},
    {'cluster':'claix23','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'1 Task'},
    ])

#Hypothesis 4: Caching
plot('Caching Comparison', 'hyp4',[
    {'cluster':'claix18','fs':'tmp','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Cached'},
    {'cluster':'claix18','fs':'tmp_odirect','n_tasks':1,'n_nodes':1,'n_files':1000,'operation':'write', 'label':'Uncached'},
    ])

#Hypothesis 5: OpenFOAM
plot('OpenFOAM Motorbike Rooflines', 'hyp5', [
    {'cluster':'claix23','fs':'tmp','n_tasks':96, 'n_nodes':1, 'operation':'write', 'label':'Local'},
    {'cluster':'claix23','fs':'beeond','n_tasks':96, 'n_nodes':1, 'operation':'write', 'label':'Ad-Hoc'},
    {'cluster':'claix23','fs':'lustre','n_tasks':96, 'n_nodes':1, 'operation':'write', 'label':'Parallel'},
    ])
