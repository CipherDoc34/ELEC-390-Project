import pandas as pd
import numpy as np
import os
import glob

path = os.path.dirname(os.path.realpath(__file__))
extension = 'csv'
result = glob.glob(path + "\\**\\*.csv")

def label(path, lenpath):
    data = pd.read_csv(path)
    
    Activity = []
    
    for i in range(len(data['Time (s)'])):
        if data['Time (s)'][i] < 30:
            Activity.append(1)
        elif data['Time (s)'][i] >= 30 and data['Time (s)'][i] < 35:
            Activity.append(0)
        elif data['Time (s)'][i] >= 35 and data['Time (s)'][i] < 65:
            Activity.append(2)
        elif data['Time (s)'][i] >= 65 and data['Time (s)'][i] < 70:
            Activity.append(0)
        elif data['Time (s)'][i] >= 70 and data['Time (s)'][i] < 100:
            Activity.append(3)
        else:
            Activity.append(0)
    data['Activity'] = Activity
    
    data.to_csv(path[:path.find('\\',lenpath+1)-len(path)] + '\\Raw Data Labeled.csv')
    

for i in result:
    label(i, len(path))