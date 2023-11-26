# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/11/26 
@time: 20:40
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from scipy.stats import ttest_ind
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FormatStrFormatter, MaxNLocator
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

# ***************************************************

def read_data():
    engine = create_engine("postgresql://diany:DotttKaixi520@127.0.0.1:5432/testdb")
    return pd.read_sql('select * from waterfall_data', con=engine).rename(columns={'index':'wafer_id'})

data = read_data()

# ***************************************************

linewidth = 3
alpha = 0.8

font_prop_legend = FontProperties(family='Times New Roman')
fontdict_legend = {'family':'Times New Roman', 'size':15}

mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.labelsize'] = 30
mpl.rcParams['xtick.labelsize'] = 30
mpl.rcParams['ytick.labelsize'] = 30
mpl.rcParams['legend.fontsize'] = 30

# ***************************************************

def proc_data(df):
    df['fp_process'] = df['6200']-df['5150']
    df['epi_process'] = df['7300']-df['6200']

    return df

data = proc_data(data[['wafer_id','5150','6200','7300']])
mean_values = data.agg('mean')

for i, site in enumerate(['5150','6200','7300']):
    plt.bar(2*i-0.3, data[site].mean(), color='C1', alpha=0.3, width=0.3)

plt.bar(1-0.3, data['fp_process'].mean(), bottom=data['5150'].mean(), color='C2', alpha=0.3, width=0.3)
plt.bar(3-0.3, data['epi_process'].mean(), bottom=data['6200'].mean(), color='C2', alpha=0.3, width=0.3)

data2 = data.copy()
data2['fp_process'] = data2['fp_process']+data2['5150'].mean()
data2['epi_process'] = data2['epi_process']+data2['6200'].mean()
data3 = pd.melt(data2, id_vars=['wafer_id'], value_vars=['5150', 'fp_process', '6200', 'epi_process', '7300'], var_name='site', value_name='value')

violin_parts = sns.violinplot(data=data3, x='site', y='value', alpha=0.2, inner=None, split=True)


for vp in violin_parts.collections[::1]:
    vp.set_alpha(0.3)
    for path in vp.get_paths():
        vertices = path.vertices
        vertices[:,0] = np.clip(vertices[:,0], np.median(vertices[:,0]), np.inf)

sns.stripplot(x='site', y='value', data=data3, jitter=True, size=4, color=".3", linewidth=0, alpha=0.1)

plt.text(1,30,'FP', ha='center')
plt.text(3,30,'EPI', ha='center')

plt.text(1, mean_values['5150']+mean_values['fp_process']+5,f"{data['fp_process'].mean():.1f}", ha='center', color='red')
plt.text(3, mean_values['6200']+mean_values['epi_process']+5,f"{data['epi_process'].mean():.1f}", ha='center', color='red')

site_list = ['5150','fp_process','6200','epi_process','7300']
for i in range(4):
    plt.plot([i,i+1],[data2[site_list[i]].mean(),data2[site_list[i]].mean()], alpha=0.3)

plt.title('Scatter & Box & Half-Violin Plot', y=1.01)
plt.xlim(-0.50,4.6)
plt.xticks([])
plt.xlabel('')
plt.ylim(-40,40)
plt.xlim(-0.8,4.5)
plt.show()

