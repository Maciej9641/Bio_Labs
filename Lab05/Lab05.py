import pandas as pd

import tensorflow as tf
from tensorflow import keras

import keras
import numpy as np

fields = ['location','date','total_cases','new_cases','total_deaths','new_deaths']
data = pd.read_csv('owid-covid-data.csv',usecols=fields)

data['date'] = pd.to_datetime(data['date'])

start_date = '2020-03-03'
end_date = '2020-05-10'
poland_data = data[data['location']=='Poland']

mask = (data['date'] > start_date) & (data['date'] <= end_date)

poland_data = poland_data.loc[mask]
poland_data = poland_data.reset_index(drop=True)
print(poland_data)

data_count = 68

total_cases = np.empty((data_count, 1, 1))
total_cases = poland_data['total_cases'].values
total_cases = (total_cases / 20000) # + 0.01 add to avoid 0 ?
print(total_cases)

days = np.empty((data_count, 1, 1))

for i in range (data_count):
    days[i] = i + 1

print(days)

input  = keras.engine.input_layer.Input(name="input", shape=(1,1))
FlattenLayer = keras.layers.Flatten()
path = FlattenLayer(input)

for i in range(0,3):
  LayerDense1 = keras.layers.Dense(20, activation=None, use_bias=True, kernel_initializer='glorot_uniform')
  path = LayerDense1(path)

  LayerPReLU1 = keras.layers.PReLU(alpha_initializer='zeros', shared_axes=None)
  path = LayerPReLU1(path)

LayerDenseN = keras.layers.Dense(1, activation=keras.activations.sigmoid, use_bias=True, kernel_initializer='glorot_uniform')
output = LayerDenseN(path)

coronaModel = keras.Model(input, output, name='coronaEstimatior')

coronaModel.summary() # Display summary

rmsOptimizer = keras.optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

coronaModel.compile(optimizer=rmsOptimizer,loss=keras.losses.MSE)

coronaModel.fit(days, total_cases, epochs=200, batch_size=1, shuffle=True)

coronaModel.save('coronaModel.h5')

