import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats
from matplotlib import rc
import nibabel as nib
import random
import pylab as py

def pp_plot(
    data, 
    title,
    c = ['#0000FF', '#FF0000','#AAAA00'],
    l = ['solid', 'solid', 'solid'],
    f = None,
    ax1 = None
):
    '''
    PP-plots of the samples. 
    '''
    if f == None and ax1 == None:
        f,(ax1) = plt.subplots(
            1,1,
            sharey=False,
            figsize=(4.5,3)
        )
    
    n=len(data[0])
    
    dist = scipy.stats.t
    beta = scipy.stats.beta
    
    p_th = -np.log10(
        [t/(n+1) for t in range(1,n+1)]
    )
    p_th_sub=-np.log10(
        [t/(n+1) for t in range(1,10001)]
    )    
        
    conf_int_inf = [
        -np.log10(beta.interval(0.95,i,n-i+1,loc=0,scale=1)[0])+np.log10(i/(n+1)) for i in range(1,10001)
    ]
    conf_int_sup = [
        -np.log10(beta.interval(0.95,i,n-i+1,loc=0,scale=1)[1])+np.log10(i/(n+1)) for i in range(1,10001)
    ]    

    line = []
    for n_data in range(len(data)):
    
        p_obs = -np.log10(
            sorted(dist.sf(np.array(data[n_data]),98))
            )

        ba_diff = [(p_obs[i] - p_th[i]) for i in range(n)]

        line.append(
            ax1.plot(p_th, ba_diff, c[n_data], 
            linestyle = l[n_data])[0]
            )
        
    ax1.plot(
        p_th,n*[0],'-'
    )
    ax1.fill_between(
        p_th_sub,
        conf_int_inf,
        conf_int_sup,
        color="lightgrey"
    )
        
    ax1.set_xlabel(
        'expected -log10(p-values)',
        fontsize=16
    )
    ax1.set_ylabel(
        'difference between observed\nand expected -log10(p-values)',
        fontsize=16
    )
    ax1.legend(
        line,
        title,
        fontsize=16
    )   

    return f, ax1


def distribution_plots(
    data, 
    title, 
    f=None,
    ax=None
):
    '''
    Distribution of p-values.
    '''
    if f == None and ax==None:
        f,ax = plt.subplots(
            1,1,
            sharey=False,
            figsize=(6,2.5)
        )
    
    dist = scipy.stats.t
    
    n, bins, patches = ax.hist(
        np.array(data),
        100,
        density=True
    )

    y=dist.pdf(
        bins,98
    )

    ax.plot(
        bins, 
        y, 
        '-'
    )

    ax.set_xlim((-5,5))

    ax.set_title(
        title,
        fontsize=16
    )

    return f
