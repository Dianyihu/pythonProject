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

test = pd.melt(data, id_vars=['wafer_id'], value_vars=['5150', 'FP_process', '6200', 'EPI_process', '7300'], var_name='site', value_name='value')

# ***************************************************

# plt.style.use(['science','no-latex'])
linewidth = 3
alpha = 0.8

font_prop_legend = FontProperties(family='Times New Roman')
fontdict_legend = {'family':'Times New Roman', 'size':15}

mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.labelsize'] = 30
mpl.rcParams['xtick.labelsize'] = 30
mpl.rcParams['ytick.labelsize'] = 30
mpl.rcParams['legend.fontsize'] = 30


plt.figure(figsize=(12,8))
palette = ['#5cc3e8','#ffdb00','#79ceb8','#e95f5c']

violin_parts = sns.violinplot(x='site',y='value',data=test,split=True,
                              inner=None,palette=palette)

shift = 0.2

for vp in violin_parts.collections[::1]:
    for path in vp.get_paths():
        vertices = path.vertices
        vertices[:,0] = np.clip(vertices[:,0], np.median(vertices[:,0]), np.inf)
        vertices[:,0] += shift

# sns.boxplot(x='site', y='value', data=test, width=0.3, fliersize=0, linewidth=1.5,
#             boxprops={'edgecolor':'black'}, palette=palette, showcaps=True, whiskerprops={'linewidth':1.5},
#             capprops={'linewidth':1.5}, medianprops={'color':'black'})

sns.barplot(x='site', y='value', data=test, width=0.3, alpha=0.5)
mean_values = test.groupby('site')['value'].mean().values
groups = ['5150','FP_process','6200','EPI_process','7300']
plt.scatter(groups, mean_values, color='white', edgecolor='black',s=80, zorder=5)
sns.stripplot(x='site', y='value', data=test, jitter=True, size=4, color=".3", linewidth=0)

# plt.axhline(y=0, linestyle='--', color='red', linewidth=1)
# plt.axhline(y=100, linestyle='--', color='red', linewidth=1)

# y, h, col = test['value'].max()+5, 5, 'k'
#
# pairs = [('5150', '6200'), ('5150', '7300'), ('6200', '7300')]
#
# for i, (group1, group2) in enumerate(pairs):
#     group1_values = test[test['site'] == group1]['value']
#     group2_values = test[test['site'] == group2]['value']
#     _, p_value = ttest_ind(group1_values, group2_values)
#
#     if p_value < 0.05:
#         x1, x2 = groups.index(group1), groups.index(group2)
#
#         plt.plot([x1, x1, x2, x2], [y + (h*i), y + h + (h*i), y + h + (h*i), y + (h*i)], lw=1.2, c=col)
#         plt.text((x1+x2)*.5, y+h+(h*i), f'p = {p_value:.3f}', ha='center', va='bottom', color=col)
#
#     y += h

plt.title('Scatter & Box & Half-Violin Plot', y=1.01)
plt.xlim(-0.50,4.6)
# plt.ylim(-50, y+h+10)
plt.xlabel('')
plt.ylabel('ERO (nm)')
plt.subplots_adjust()
plt.tight_layout()
plt.show()

