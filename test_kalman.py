# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/9/16 
@time: 00:51
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from kalman_filter import Kalman_filter

data = pd.read_pickle('data.pkl')

data['delta_date'] = (data['Date'] - data['Date'].shift())/pd.Timedelta(1, 'day')
data['delta_T_PK'] = data['T_PK'] - data['T_PK'].shift()
data['delta_T_AV'] = data['T_AV'] - data['T_AV'].shift()
data['k_T_PK'] = data['delta_T_PK']/data['delta_date']
data['k_T_AV'] = data['delta_T_AV']/data['delta_date']

ts = data[['delta_date', 'T_PK', 'k_T_PK']].head(500).dropna().to_numpy()

# sns.scatterplot(data=data, x='Date', y='k_T_PK')
# plt.show()

A = np.eye(2)
H = np.array([[1,0]])

x0 = np.array([[15,0]]).T
p0 = np.array([[10,0],[0,100]])
Q = np.array([[10,0],[0,10]])
R = np.array([[100]])

# kf = Kalman_filter(A, Q, H, R, x0, p0)
# kf.filter(z_list=ts)

kf = Kalman_filter(A, Q, H, R, x0, p0)
z_list = ts
u_list = np.zeros(z_list.shape[0]).reshape(-1, 1)

for u_1, z_1 in zip(u_list, z_list):
    kf.update_matrix(A=np.array([[1,z_1[0]],[0,1]]))
    xhat_10, phat_10 = kf.predict(kf.xhat[:, [-1]], kf.phat[-1], u_1)
    xhat_1, phat_1 = kf.update(xhat_10, phat_10, z_1[[1]].reshape(-1, 1))

    kf.xhat = np.append(kf.xhat, xhat_1, axis=1)
    kf.phat = np.append(kf.phat, np.expand_dims(phat_1, axis=0), axis=0)

x = range(499)
y_actual = ts[:,1].reshape(-1)
y_predicted = kf.xhat[0].reshape(-1)[1:]

sns.scatterplot(x=x, y=y_actual)
sns.lineplot(x=x, y=y_predicted, color='C1')
plt.show()

y_actual2 = ts[:,2].reshape(-1)
y_predicted2 = kf.xhat[1].reshape(-1)[1:]

sns.scatterplot(x=x, y=y_actual2)
sns.lineplot(x=x, y=y_predicted2, color='C1')
plt.show()
