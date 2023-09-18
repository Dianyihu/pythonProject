# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/9/18 
@time: 21:25
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pykalman import KalmanFilter

data = pd.read_pickle('data.pkl')

kf = KalmanFilter(transition_matrices=[1], transition_covariance=[1e-1],
                  observation_matrices=[1], observation_covariance=[1],
                  initial_state_mean=15, initial_state_covariance=25)

measurements = data['T_AV'].head(500)

filtered_state_estimates = kf.filter(measurements)[0]
smoothed_state_estimates = kf.smooth(measurements)[0]

sns.scatterplot(x=range(500), y=measurements)
sns.lineplot(x=range(500), y=filtered_state_estimates.reshape(-1), color='C1')
plt.show()

sns.scatterplot(x=range(500), y=measurements)
sns.lineplot(x=range(500), y=smoothed_state_estimates.reshape(-1), color='C1')
plt.show()

mean, covariance = kf.filter(measurements)