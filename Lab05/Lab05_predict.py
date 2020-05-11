import tensorflow as tf
from tensorflow import keras

import keras
from keras.models import load_model
import numpy as np

coronaModel = load_model('coronaModel.h5')
coronaModel.summary()

new_day = np.empty((1,1,1))
new_day[0,0,0] = 69

case_number = coronaModel.predict(new_day)
case_number = case_number*20000 #renormalize data

print(case_number)

np.savetxt('case_number.txt',case_number,fmt='%f')

