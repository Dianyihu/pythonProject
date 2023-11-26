# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/11/26 
@time: 19:54
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

def read_data():
    engine = create_engine("postgresql://diany:DotttKaixi520@127.0.0.1:5432/testdb")
    return pd.read_sql('select * from waterfall_data', con=engine).rename(columns={'index':'wafer_id'})

data = read_data()

test = pd.melt(data, id_vars=['wafer_id'], value_vars=['5150', 'FP_process', '6200', 'EPI_process', '7300'], var_name='site', value_name='value')


sns.violinplot(data=test, x='site', y='value')
plt.show()




