# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2024/1/3 
@time: 21:27
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm

cmap = cm.coolwarm


# ***************************************************

esfqr = pd.Series(35+10*np.random.rand(72), index=np.arange(0,360,5))
sfqr = pd.read_pickle('sfqr.pkl')

sfqr.columns = [int(i) for i in sfqr.columns]
sfqr.index = [int(i) for i in sfqr.index]

# ***************************************************

def paint_sfqr(df, ax):
    for y, row in df.iterrows():
        for x, value in row.items():
            ax.barh(4+8*y, 26, height=8, left=26*int(x), color=cmap(value/50) if not np.isnan(value) else 'w',alpha=0.6)

def paint_esfqr(ser, ax):
    for angle, value in ser.items():
        ax.barh(140.5, 5*np.pi/180, left=(angle-2.5)*np.pi/180, height=15, color=cmap(value/50), alpha=0.6)


def centering_data(data, mode):
    df_reverse = data.copy()
    match mode:
        case ('sfqr', 0):
            for i in df_reverse.index:
                for j in df_reverse.columns:
                    df_reverse.iat[i,j] = data.iat[i,j] - data.iat[-1-i,-1-j]
            return abs(df_reverse.loc[:0, :])

        case ('sfqr', 1):
            for i in df_reverse.index:
                for j in df_reverse.columns:
                    df_reverse.iat[i,j] = data.iat[i,j] - data.iat[-1-i,j]
            return abs(df_reverse.loc[:, 0:])

        case ('sfqr', 2):
            for i in df_reverse.index:
                for j in df_reverse.columns:
                    df_reverse.iat[i,j] = data.iat[i,j] - data.iat[i,-1-j]
            return abs(df_reverse.loc[:0, :])

        case ('esfqr', 0):
            for i in df_reverse.index:
                df_reverse.loc[i] = data.loc[i] - data.loc[(i+180)%360]
            return df_reverse

        case ('esfqr', 1):
            for i in df_reverse.index:
                if 360-i in df_reverse.index:
                    df_reverse.loc[i] = data.loc[i] - data.loc[360-i]

            return abs(df_reverse[(df_reverse.index>0)&(df_reverse.index<180)])

        case ('esfqr', 2):
            for i in df_reverse.index:
                if i<180 and 180-i in df_reverse.index:
                    df_reverse.loc[i] = data.loc[i] - data.loc[180-i]
                elif i>=180 and 540-i in df_reverse.index:
                    df_reverse.loc[i] = data.loc[i] - data.loc[540-i]

            return abs(df_reverse[(df_reverse.index<90)|(df_reverse.index>270)])



# ***************************************************

fig = plt.figure(figsize=(16, 12))

ax0 = fig.add_axes([0.05,0.52,0.3,0.45], aspect='equal')
paint_sfqr(sfqr, ax0)

ax1 = fig.add_axes([0.05,0.52,0.3,0.45], polar=True, aspect='equal')
paint_esfqr(esfqr, ax1)

ax2 = fig.add_axes([0.38,0.52,0.3,0.45], polar=True, aspect='equal')
ax2.plot(esfqr.index.to_numpy()*np.pi/180, esfqr.values)

ax3 = fig.add_axes([0.71,0.52,0.3,0.45], polar=True, aspect='equal')
ax3.plot(esfqr.index.to_numpy()*np.pi/180, esfqr.values)

ax4 = fig.add_axes([0.05,0.02,0.3,0.45], polar=True, aspect='equal')
symmetry1 = centering_data(esfqr, ('esfqr', 0))
paint_esfqr(symmetry1, ax4)

ax5 = fig.add_axes([0.38,0.02,0.3,0.45], polar=True, aspect='equal')
symmetry2 = centering_data(esfqr, ('esfqr', 1))
paint_esfqr(symmetry2, ax5)

ax6 = fig.add_axes([0.71,0.02,0.3,0.45], polar=True, aspect='equal')
symmetry3 = centering_data(esfqr, ('esfqr', 2))
paint_esfqr(symmetry3, ax6)

# ***************************************************

ax1.set_ylim(0, 150)
ax1.set_yticks([])
ax0.set_xticks([])
ax0.set_yticks([])
ax1.spines.clear()
ax0.spines.clear()

ax0.set_xlim(-150, 150)
ax0.set_ylim(-150, 150)

ax0.patch.set_alpha(0)
ax1.patch.set_alpha(0)

plt.show()