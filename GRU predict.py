# endcoding: utf-8

'''
Created by
@author: Dianyi Hu
@date: 2023/9/17 
@time: 01:54
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import GRU, Dense
from keras.callbacks import EarlyStopping

T = 6
HORIZON = 1
LATENT_DIM = 5
BATCH_SIZE = 32
EPOCHS = 10

model = Sequential()
model.add(GRU(LATENT_DIM, input_shape=(T, 1)))
model.add(Dense(HORIZON))

model.compile(optimizer='RMSprop', loss='mse')
model.summary()

GRU_earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5)
model.history = model.fit(X_train, y_train,
                          batch_size=BATCH_SIZE,
                          epochs=EPOCHS,
                          validation_data=(X_valid, y_valid),
                          callbacks=[GRU_earlystop],
                          verbose=1)

# ***************************************************
# ***************************************************

