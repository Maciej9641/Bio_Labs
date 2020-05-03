#Sieć neuronowa

#Bibioteki do obliczen tensorowych

import tensorflow as tf
from tensorflow import keras

# import plaidml.keras
# plaidml.keras.install_backend()

#Bibioteka do obsługi sieci neuronowych
import keras

#Załadowania bazy uczącej
import imageio
import numpy as np
import pandas as pd

import os

from keras.models import load_model

# returns a compiled model
# identical to the previous one
genderModel = load_model('genderModel.h5')
genderModel.summary() # Display summary

imgCount = 49
ImgWidth = 100
ImgHeight = 100

BazaImg = np.empty((imgCount,ImgHeight,ImgWidth,3))
i=0
#FileName = ".\\baza_testowa\\k\\01.png"
dirList = os.listdir(".\\baza_testowa\\k")
for dir in dirList:
    FileName = ".\\baza_testowa\\k\\{}".format(dir)
    Img = imageio.imread(FileName)
    Img = (Img / 127.5) - 1
    BazaImg[i,:,:,:] = Img[0:ImgHeight,0:ImgWidth,0:3]
    i = i+1

#FileName = ".\\baza_testowa\\m\\01.png"
dirList = os.listdir(".\\baza_testowa\\m")
for dir in dirList:
    FileName = ".\\baza_testowa\\m\\{}".format(dir)
    Img = imageio.imread(FileName)
    Img = (Img / 127.5) - 1
    BazaImg[i,:,:,:] = Img[0:ImgHeight,0:ImgWidth,0:3]
    i = i+1

gender = genderModel.predict(BazaImg) # 0 - m, 1 - k
print(gender)
gender_real = []
true_predictions = 0

for i in range(imgCount):
    if(i<25):
        gender_real.append(1)
        if(gender[i,0]>0.5):
            true_predictions = true_predictions + 1
    else:
        gender_real.append(0)
        if(gender[i,0]<0.5):
            true_predictions = true_predictions + 1

model_prediction_rate = true_predictions*100/imgCount
data = {'gender_real': gender_real,
        'gender_predicted': gender[:,0]}

data2 = {'true_predictions': true_predictions,
         'model_prediction_rate': model_prediction_rate}

df = pd.DataFrame(data, columns= ['gender_real', 'gender_predicted'])
df = df.append(data2, ignore_index=True)

df = df.replace(np.nan, '', regex=True)

print(df)

df.to_csv('results.csv')

np.savetxt('results.txt', df.values, fmt='%s',
 delimiter='\t\t\t', header= "gender_real\tgender_predicted\tmodel_prediction_rate\ttrue_predictions" )

#50
#--------------------------------
# Prawdziwa Płeć | Odpowiedz sieci
#----------------+---------+------
#                |   M     |  K
#----------------+---------+------
#   M            |         |  1
#----------------+---------+------
#   K            |         |  1
