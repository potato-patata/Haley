# -*- coding: utf-8 -*-
"""diseaseprediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-dKZ1BsK_FS0ewsllFMiE3BtbT4UF550
"""

#if you are not using google collab please ignore this
#to mount google drive
from google.colab import drive
drive.mount('/content/drive')

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import csv,numpy as np,pandas as pd
import os

data = pd.read_csv("/content/drive/My Drive/Group_Project/Training.csv")

df = pd.DataFrame(data)
cols = df.columns
cols = cols[:-1]
x = df[cols]
y = df['Disease']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

print ("DecisionTree")
dt = DecisionTreeClassifier()
clf_dt=dt.fit(x_train,y_train)
#print ("Acurracy: ", clf_dt.score(x_test,y_test))

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
    user_input_label = user_input_label.reshape((-1,1)).transpose()
    return(dt.predict(user_input_label))

#print(dosomething(['Sneezing', 'Sore Throat', 'Stuffy Nose' ]))
#prediction = []
#for i in range(7):
#    pred = dosomething(['Sneezing', 'Sore Throat', 'Stuffy Nose'])   
#    prediction.append(pred) 
#print(prediction)