# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 13:25:16 2023

@author: Keshav
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import requests
import joblib
import dill as pickle
import numpy as np
# attributes = 'accX=173.66593|acc_time&acc_time=173.66593&accY=173.66593|acc_time&accZ=173.66593|acc_time'
attributes = 'accX&accY&accZ&acc_time'
r = requests.get("http://192.168.50.110:8080/get?" + attributes)

json = r.json()
# print(json)
# print(json["buffer"]["accX"]["buffer"][0])
style.use('fivethirtyeight')

model = joblib.load('E:\\Desktop\\390\\ELEC-390-Project\\log_reg_model.pkl')
with open('E:\\Desktop\\390\\ELEC-390-Project\\preprocessing_features.pkl', 'rb') as file:
    preprocessing_features = pickle.load(file)


fig, (ax, ay, az) = plt.subplots(3, 1)
X = []
Y = []
Z = []
time = []
Xpart = []
Ypart = []
Zpart = []
timepart = []
flag = 0
def animate(i):
    attributes = 'accX&accY&accZ&acc_time'
    r = requests.get("http://192.168.50.110:8080/get?" + attributes)
    json = r.json()
    global flag
    global Xpart
    global Ypart
    global Zpart
    global timepart
    if (len(json)):
        t = json["buffer"]["acc_time"]["buffer"][0]
        accx = json["buffer"]["accX"]["buffer"][0]
        accy = json["buffer"]["accY"]["buffer"][0]
        accz = json["buffer"]["accZ"]["buffer"][0]
        
        if(int(t) % 5 == 0 and not flag):
            flag = 1
            data = pd.DataFrame(columns=["time", "x", "y", "z", "acc"])
            data["time"] = time
            data["x"] = X
            data["y"] = Y
            data["z"] = Z
            print(data)
            features = preprocessing_features(data).features
            print(features)
            prediction = model.predict(features)
            print(prediction)
        elif(int(t) % 5 != 0):
            flag = 0
        X.append(accx)
        Y.append(accy)
        Z.append(accz)
        time.append(t)
        Xpart.append(accx)
        Ypart.append(accy)
        Zpart.append(accz)
        timepart.append(t)
        
    else:
        return
    ax.clear()
    ay.clear()
    az.clear()
    ax.plot(time, X, linewidth=1, color="red")
    ay.plot(time, Y, linewidth=1, color="blue")
    az.plot(time, Z, linewidth=1, color="green")
    
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()