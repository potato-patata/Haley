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

# %matplotlib inline

df = pd.read_csv("/content/drive/My Drive/Group_Project/filename.csv")

#splitting categorical column and numerical column 
#normalising numerical columns and then merging again.
target_col = ["Disease"]
cat_cols   = df.nunique()[df.nunique() < 6].keys().tolist()
cat_cols   = [x for x in cat_cols if x not in target_col]
num_cols   = [x for x in df.columns if x not in cat_cols + target_col]
min_max_scaler = preprocessing.MinMaxScaler()
scaled = min_max_scaler.fit_transform(df[num_cols])
scaled = pd.DataFrame(scaled,columns=num_cols)

#dropping original values merging scaled values for numerical columns
df_og = df.copy()
df = df.drop(columns = num_cols,axis = 1)
df = df.merge(scaled,left_index=True,right_index=True,how = "left")

column_names_full = ['Sweating',
 'Nosebleed',
 'Confusion',
 'Mucus',
 'Loss of Appetite',
 'Loss of Smell',
 'Loss of Taste',
 'Hoarseness',
 'Muscle Weakness',
 'Increase sensitivity to cold',
 'Low Body Temperature',
 'Cold',
 'Trouble sleeping',
 'Allergy',
 'Fluid accumulation',
 'Vision problems',
 'Weakness',
 'Unexplained Bleeding',
 'Unexplained Bruising',
 'Itchy nose',
 'Itchy mouth',
 'itchy throat',
 'Irritable',
 'Dandruff',
 'Night Sweats',
 'Mouth Ulcers',
 'Interrupting',
 'Avoiding activities',
 'Skin discoloration',
 'Oily Skin',
 'Obesity',
 'Short tempered',
 'Dizziness',
 'Blood in urin',
 'Infection',
 'Irritable.1',
 'Depression',
 'Anxiety',
 'Forgetfulness',
 'Low Blodd pressure',
 'Dry mouth',
 'Muscle Cramps',
 'Dehydration',
 'Sneezing',
 'Stuffy Nose',
 'Sore Throat',
 'Cough',
 'Phlegm',
 'Body Pain',
 'Fatigue',
 'Headache',
 'Chills',
 'Fever',
 'Irregular Periods',
 'Excessive hair growth',
 'Chest Pain',
 'Weight Gain',
 'Chest Discomfort',
 'Shortness of Breath',
 'Puffy Face',
 'Constipation',
 'Nausea',
 'Vomiting',
 'Diarrhea',
 'Wheezing',
 'Swelling',
 'Muscle Ache',
 'Rash',
 'Rashes',
 'Red Spots',
 'Itchy',
 'Eye pain',
 'Increase of sweating',
 'Itchy Eyes',
 'Running nose',
 'Unresponsiveness',
 'Unfocused',
 'Impulsiveness',
 'Fidgeting',
 'Easily Distracted',
 'High blood pressure',
 'Muscle Pain',
 'Decrease range of Motion',
 'Indigestion',
 'Abdominal pain',
 'Whiteheads',
 'Pain during urination',
 'Frequent Urination',
 'Difficulty Urinating',
 'Blackheads',
 'Cystic lesions',
 'Pimples',
 'Redness',
 'Tiredness',
 'Sleeplessness',
 'Daytime sleepiness',
 'Pain',
 'Dry Skin',
 'Missed menstrual cycle',
 'Stiffness',
 'Disease']
df = df.reindex(columns=column_names_full)

df.head

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

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    encoded_Y,
                                                    test_size=.40,
                                                    random_state=42, stratify = encoded_Y)

X_train_res, y_train_res = X_train, y_train.ravel()
dfx_train=pd.DataFrame(data=X_train_res)
dfy_train=np.reshape(y_train_res,[y_train_res.shape[0],1])
dfx_test=pd.DataFrame(data=X_test)
dfy_test=y_test

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

lenet = Sequential()
#input_shape = X_train1[0].shape
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

Ytest.shape

print(lenet.summary())

from sklearn.model_selection import  ShuffleSplit, cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report

lenet.compile(loss='sparse_categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
lenet.fit(Xtrain, Ytrain, batch_size=32, epochs=5, verbose = 1 ,validation_data = (Xtest,Ytest))

lss = 0
acc = 0
precision = 0
recall = 0
specificity = 0
sensitivity = 0
fm = 0
dd = 0
score = lenet.evaluate(Xtest, Ytest, verbose=0)
#nested_score = cross_val_score(lenet, X=Xtest, y=Ytest, cv=cv1, scoring=make_scorer(classification_report_with_accuracy_score))
lss += score[0]
acc += score[1]
print("Test Score:", lss)
print("Test Accuracy:", acc)
'''
#ignore this chunk for now 
y_pred = lenet.predict(Xtest)
#y_pred = np.argmax(y_pred)
#y_test = np.argmax(Ytest)
#y_test = Ytest
conf= confusion_matrix(y_test,y_pred)
print(conf)
precisionValue = conf[1,1]/(conf[1,1]+conf[0,1])
precision += precisionValue
print(',Precision Value = ', precisionValue,end = " ")
    #Recall = TP / TP+FN
RecallValue = conf[1,1]/(conf[1,1]+conf[1,0])
recall += RecallValue
print('Recall Value = ,',RecallValue,end = " ")
    #Specificity = TN / (FP + TN)
SpecificityValue = conf[0,0]/(conf[0,1]+conf[0,0])
specificity += SpecificityValue
print('Specificity Value = ,',SpecificityValue,end = " ")
    #Sensitivity = TP / (TP + FN)
SensitivityValue = conf[1,1]/(conf[1,1]+conf[1,0])
sensitivity += SensitivityValue
print('Sensitivity Value = ,',SensitivityValue,end = " ")
    # F1 measure
fmeasure = 2 * (precisionValue*RecallValue) / (precisionValue + RecallValue)
fm += fmeasure
print('f measure = ,',fmeasure)
print(classification_report(y_test,y_pred))
'''