# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/11/26 
@time: 19:37
'''

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("postgresql://diany:DotttKaixi520@127.0.0.1:5432/testdb")

columns = ['5150', 'FP_process', '6200', 'EPI_process', '7300']

data = pd.DataFrame(columns=columns)
data['5150'] = 20*np.random.random(100)-20
data['FP_process'] = 5*np.random.random(100)-5
data['6200'] = data['5150'] + data['FP_process']
data['EPI_process'] = 2*np.random.random(100)+20
data['7300'] = data['6200'] + data['EPI_process']

data.to_sql('waterfall_data',schema='public',con=engine,if_exists='replace')