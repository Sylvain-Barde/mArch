# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 08:59:05 2024

This files provides a demo for the fast implementation of the Multivariate
extension for the 'arch' toolbox. It uses the Oxford-Man realized volatility 
library of Heber et. al 2009, version 0.3:

Heber, Gerd, Asger Lunde, Neil Shephard and Kevin K. Sheppard (2009) 
"Oxford-Man Institute's realized library", Oxford-Man Institute, University of 
Oxford.


@author: Sylvain Barde, University of Kent
"""

import pandas as pd

from mArch import mArch
from arch.univariate import GARCH
from matplotlib import pyplot as plt

# Set some parameters
dataPath = 'data/oxfordmanrealizedvolatilityindices.csv'
indList = ['.SPX', '.FTSE', '.N225']     # Database indices
numObs = 2700
splitObs = 2500

fontSize = 32
y_min = -12
y_max = 12

# Load dataset, extract indices, format data
data = pd.read_csv(dataPath, index_col=[0])

for count,ind in enumerate(indList):
    if count == 0:
        mRt = pd.DataFrame(          # Daily returns (for sign)
                data[data.Symbol == ind]['open_to_close']
                ).rename(columns={"open_to_close": ind})

    else:
        mRt = mRt.merge(pd.DataFrame(
            data[data.Symbol == ind]['open_to_close']
            ).rename(columns={"open_to_close": ind}),
                        how='inner', 
                        left_index = True, 
                        right_index = True)
mRt *= 100                              # Rescale to % from raw log-returns
mRt.index = pd.to_datetime(mRt.index)   # Change index to datetime for plot

# Plot the data
for ind in indList:
    xlim_left = mRt.index[0]
    xlim_right = mRt.index[numObs]
        
    fig = plt.figure(figsize=(16,12))
    ax = fig.add_subplot(1, 1, 1)
    ax.fill([mRt.index[splitObs],
             xlim_right,
             xlim_right,
             mRt.index[splitObs]], 
            [y_min,y_min,y_max,y_max], 
            color = 'k', alpha=0.15, label = r'Testing sample')
    ax.plot(mRt.index[0:numObs], mRt.iloc[0:numObs][ind], 
            'b', linewidth=1,label =  '{:s} % daily return'.format(ind))
    ax.set_ylim([y_min,y_max])
    ax.legend(loc='upper left', frameon=False, prop={'size':fontSize})
    ax.set_ylim(top = y_max, bottom = y_min)
    ax.set_xlim(left = xlim_left,right = xlim_right)
    ax.plot(xlim_right, y_min, ">k", ms=15, clip_on=False)
    ax.plot(xlim_left, y_max, "^k", ms=15, clip_on=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.tick_params(axis='x', pad=15, labelsize=fontSize)
    ax.tick_params(axis='y', pad=15, labelsize=fontSize)
        
# Create mArch estimation object by loading data
mArchEst = mArch(mRt.iloc[0 : numObs])

# Setup the estimation, providing the univariate specification, the error type
# and the multivariate specification
univarSpec = GARCH(p = 2, q = 2, o = 1, power = 2)
mArchEst.setArch(univarSpec,
                 errors = 'Student', 
                 multivar = 'dcca')

# Run the estimation with a user-provided starting point for the DCCA 
# parameters
initVals = [0.05, 0.9, 0.05 ,7]
mArchEst.fit(update_freq = 0, 
             last_obs = splitObs,
             init = initVals)

# Check boundary condition and print the estimation summary
mArchEst.checkBoundary()
mArchEst.summary()

# Generate a 5-day ahead forecast
forecastMethod = 'simulation'
Hpred = mArchEst.forecast(horizon = 5, 
                          start = splitObs, 
                          method = forecastMethod)