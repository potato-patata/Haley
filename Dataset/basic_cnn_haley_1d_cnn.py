# -*- coding: utf-8 -*-
"""basic_cnn_haley

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19OQCrpki7o-wEkUFZjUYfCNWyCtw3qX-
"""

#if you are not using google collab please ignore this
#to mount google drive
from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
#Normalization
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from keras.models import Sequential
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import tensorflow as tf
from keras.models import *
from keras.layers import *
from keras.callbacks import *
from sklearn.model_selection import  ShuffleSplit, cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report

# %matplotlib inline

#df = pd.read_csv("/content/drive/My Drive/Group_Project/filename.csv")
data = pd.read_csv("/content/drive/My Drive/Group_Project/Binary-200row.csv")

df = pd.DataFrame(data)

#Convert dataframe to image format
def df_image(df,nt):
    dft=df.loc[df.index.repeat(pd.Series([nt]*df.shape[0]))]
    g = dft.groupby(dft.index).cumcount()
    dfz = (dft.set_index([dft.index,g]).
           unstack(fill_value=0).stack().
           groupby(level=0).
           apply(lambda x: x.values.tolist()).
           tolist())
    return dfz

X = np.array(df.iloc[:, df.columns != 'Disease'])
y = np.array(df.iloc[:, df.columns == 'Disease'])
 
# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y)
encoded_Y = encoder.transform(y)
# convert integers to dummy variables (i.e. one hot encoded)
#dummy_y = np_utils.to_categorical(encoded_Y)

#train-test split
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    encoded_Y,
                                                    test_size=.20,
                                                    random_state=42, stratify = encoded_Y)

#indexing classes
values=np.unique(df['Disease'])
values

#flattening the arrays for 1d-cnn

X_train_res, y_train_res = X_train, y_train.ravel()
dfx_train=pd.DataFrame(data=X_train_res)
dfy_train=np.reshape(y_train_res,[y_train_res.shape[0],1])
dfx_test=pd.DataFrame(data=X_test)
dfy_test=pd.DataFrame(data = y_test)



#converting df to image
np.save('train_ima_ch.npy',df_image(dfx_train,1))
np.save('train_lab_ch.npy',dfy_train)
np.save('test_ima_ch.npy',df_image(dfx_test,1))
np.save('test_lab_ch.npy',dfy_test)
Xtrain = np.load('train_ima_ch.npy')
Ytrain = np.load('train_lab_ch.npy')
Xtest = np.load('test_ima_ch.npy')
Ytest = np.load('test_lab_ch.npy')

Xtrain = np.reshape(Xtrain,[Xtrain.shape[0],100,1])
Xtest = np.reshape(Xtest,[Xtest.shape[0],100,1])
I = Ytrain[:,0].astype(int)
Ytrain = np.zeros([Xtrain.shape[0],np.unique(Ytrain).size])
Ytrain[np.arange(Ytrain.shape[0]),I] = 1

I = Ytest[:,0].astype(int)
Ytest = np.zeros([Xtest.shape[0],np.unique(Ytest).size])
Ytest[np.arange(Ytest.shape[0]),I] = 1

#1d-CNN model
lenet = Sequential()
#Input_shape = Xtrain[0].shape
lenet.add(Conv1D(filters = (100),kernel_size = 3, padding = 'same',batch_input_shape = (None,100,1), strides = 1, activation = 'relu'))
                                #Rect(),\
                                #SumPool(pool=(1,1),stride=(1,1)),\
lenet.add(Conv1D(filters = (200),kernel_size = 3, strides = 1, activation = 'relu'))
                                #Rect(),\
                                #SumPool(pool=(2,2),stride=(2,2)),\
lenet.add(Conv1D(filters = (300),kernel_size = 3, strides = 1,activation = 'relu'))
                                #Rect(),\
                                #SumPool(pool=(2,2),stride=(2,2)),\
lenet.add(Dropout(rate=0.2))
lenet.add(Flatten())
                                #Convolution(filtersize=(1,1,10,2),stride = (1,1)),\
                                #Linear(650,300),\
                                #Linear(720,10),\
                                #SoftMax(),
                                #Linear(10,2),\
lenet.add(Dense(1000, activation = 'relu'))
lenet.add(Dropout(rate=0.2))
lenet.add(Dense(25, activation = 'softmax'))
#lenet.add(Dense(1))


print(lenet.summary())

lenet.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])
lenet.fit(Xtrain, Ytrain, batch_size=32, epochs=5, verbose = 1 ,validation_data = (Xtest,Ytest))

indices = [i for i in range(100)]
symptoms = df.columns.values[:-1]

dictionary = dict(zip(symptoms,indices))

def dosomething(symptom):
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(100)]
    for i in user_input_symptoms:
        idx = dictionary[i]
        user_input_label[idx] = 1

    user_input_label = np.array(user_input_label)
    user_input_label = user_input_label.reshape((1,100,-1)).transpose()
    return(lenet.predict(user_input_label))

ds = dosomething(['Fatigue','Diarrhea','Constipation'])
#ds = disease_prediction.predict(user_input_label)
L = np.argsort(-ds, axis=1)

print(values[L[:,0]])
print(values[L[:,1]])
print(values[L[:,2]])

print(ds[0,L[:,0]]*100)
print(ds[0,L[:,1]]*100)
print(ds[0,L[:,2]]*100)

print(dosomething(['Sneezing', 'Sore Throat', 'Stuffy Nose']))

lenet.save('haley_cnn.h5')  # creates a HDF5 file 'haley_cnn.h5'
