# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 16:31:32 2023

@author: Keshav
"""

def SplitFeature(df):
    return df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]

import h5py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, \
    RocCurveDisplay, roc_auc_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
import data_extracting_features as de
import data_pre_processing as dpp
import data_visualization as dv
import data_processing as dp
import data_classifier as dc
import joblib
import numpy as np
#%%

with h5py.File("alldata.h5", "r") as f:
    test = pd.DataFrame(f["dataset"]["Test"])
    train = pd.DataFrame(f["dataset"]["Train"])


#%%
data = pd.concat([test,train])
#%%
# =============================================================================
# dropped = []
# for i in range(len(data)):
#     if(data.iloc[i, 6] < 2):
#         dropped.append(i)
# data = data.drop(labels=dropped)
# =============================================================================
#%%
data = data.loc[data[6] >= 2]
#%%
labels = data.iloc[:, -1]
X = data.iloc[:, 2:-2]

#%%
features = pd.DataFrame(columns=['meanX', 'meanY', 'meanZ',
                                 'stdX', 'stdY', 'stdZ',
                                 'maxX', 'maxY', 'maxZ',
                                 'minX', 'minY', 'minZ',
                                 'kurtX', 'kurtY', 'kurtZ',
                                 'skewX', 'skewY', 'skewZ',
                                 'rmsX', 'rmsY', 'rmsZ',
                                 'medianX', 'medianY', 'medianZ',
                                 'diffX', 'diffY', 'diffZ',
                                 'diffabsX', 'diffabsY', 'diffabsZ',
                                 'varianceX', 'varianceY', 'varianceZ'])

window_size = 500

mean = X.rolling(window=window_size).mean()
#%%
def difference(x):
    return x.iloc[-1] - x.iloc[0]
def difference_abs(x):
    return abs(x.iloc[-1] - x.iloc[0])


std = X.rolling(window=window_size).std()
max = X.rolling(window=window_size).max()
min = X.rolling(window=window_size).min()
kurt = X.rolling(window=window_size).kurt()
skew = X.rolling(window=window_size).skew()
rms = X.pow(2).rolling(window=window_size).mean().apply(np.sqrt, raw=True)
median = X.rolling(window=window_size).median()
diff = X.rolling(window=window_size).apply(difference)
diff_abs = X.rolling(window=window_size).apply(difference_abs)
variance = X.rolling(window=window_size).std()**2

#%%
features["meanX"], features["meanY"], features["meanZ"] = SplitFeature(mean)
features["stdX"], features["stdY"], features["stdZ"] = SplitFeature(std)
features["maxX"], features["maxY"], features["maxZ"] = SplitFeature(max)
features["minX"], features["minY"], features["minZ"] = SplitFeature(min)
features["kurtX"], features["kurtY"], features["kurtZ"] = SplitFeature(kurt)
features["skewX"], features["skewY"], features["skewZ"] = SplitFeature(skew)
features['rmsX'], features['rmsY'], features['rmsZ'] = SplitFeature(rms)
features['medianX'], features['medianY'], features['medianZ'] = SplitFeature(median)
features['diffX'], features['diffY'], features['diffZ'] = SplitFeature(diff)
features['diffabsX'], features['diffabsY'], features['diffabsZ'] = SplitFeature(diff_abs)
features['varianceX'], features['varianceY'], features['varianceZ'] = SplitFeature(variance)

#%%
features = features.dropna()
#%%
X_train, X_test, y_train, y_test = \
    train_test_split(features, labels[-len(features):], test_size = 0.3, shuffle=False, random_state=0)
#%%
X_train, X_test, y_train, y_test = \
    train_test_split(X, labels, test_size = 0.3, shuffle=False, random_state=0)
#%%
scaler = StandardScaler()
l_reg = LogisticRegression(max_iter=10000)
clf = make_pipeline(StandardScaler(), l_reg)

#%%
scaler = StandardScaler()
clf = RandomForestClassifier(n_estimators=100)
#%%

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_clf_prob = clf.predict_proba(X_test)

#%%
print("y_pred is: ", y_pred)
print('y_clf_prob is: ', y_clf_prob)

acc = accuracy_score(y_test, y_pred)
print("accuracy is: ", acc)

# recall = recall_score(y_test, y_pred)
# print('recall is: ', recall)

# fscore = f1_score(y_test, y_pred)
# print("F score is: ", fscore)

cm = confusion_matrix(y_test, y_pred)
cm_display = ConfusionMatrixDisplay(cm).plot()

fpr, tpr, _ = roc_curve(y_test, y_clf_prob[:, 1], pos_label=clf.classes_[1])
roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()

plt.show()

auc = roc_auc_score(y_test, y_clf_prob[:,1])
print("the AUC is: ", auc)
#%%
joblib.dump(clf, 'log_reg_model.pkl')
