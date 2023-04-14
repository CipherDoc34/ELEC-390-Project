# -*- coding: utf-8 -*-
import h5py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, \
    RocCurveDisplay, roc_auc_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

def SplitFeature(df):
    return df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]

####################### Data Visualization #######################################################
with h5py.File('alldata.h5', 'r') as hdf:
    train_data = hdf['dataset']['Train']
    column_names = hdf['dataset']['Train'].attrs['column_names']
    train_data_df = pd.DataFrame(train_data, columns=column_names)
    print(train_data_df.shape[0])

start = 0
end = 290000
window_size = 5

activity_data = {#0: train_data_df[train_data_df['Activity'] == 0],  #transition
                 1: train_data_df[train_data_df['Activity'] == 1],  #standing
                 2: train_data_df[train_data_df['Activity'] == 2],  #walking
                 3: train_data_df[train_data_df['Activity'] == 3]}  #jumping

accel_axes = ['Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)','Absolute acceleration (m/s^2)']

fig, axes = plt.subplots(3, 4, figsize=(15, 15))


for i, activity in enumerate(activity_data.keys()):
    for j, accel_axis in enumerate(accel_axes):
        activity_data[activity].loc[:, f'{accel_axis}_MA'] = activity_data[activity][accel_axis].rolling(window=window_size).mean()
        
        # Plot original data
        axes[i][j].scatter(activity_data[activity].iloc[start:end]['Time (s)'], activity_data[activity].iloc[start:end][accel_axis], label='Original')
        
        # Plot filtered data
        axes[i][j].scatter(activity_data[activity].iloc[start:end]['Time (s)'], activity_data[activity].iloc[start:end][f'{accel_axis}_MA'], label='Moving Average')
        
        axes[i][j].set_title(f"Activity {activity}: {accel_axis}")
        axes[i][j].legend()

        
        

plt.tight_layout()
plt.show()


####################### Pre Processing #######################################################
with h5py.File('alldata.h5', "r") as f:
    test = pd.DataFrame(f["dataset"]["Test"])
    train = pd.DataFrame(f["dataset"]["Train"])


data = pd.concat([test,train])
data = data.loc[data[6] >= 2]
labels = data.iloc[:, -1]
labels = labels.replace(2,0)
labels = labels.replace(3,1)

X = data.iloc[:, 2:-2]

####################### Feature Extraction #######################################################
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
def difference(x):
    return x.iloc[-1] - x.iloc[0]
def difference_abs(x):
    return abs(x.iloc[-1] - x.iloc[0])

mean = X.rolling(window=window_size).mean()
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

features = features.dropna()

####################### Model Training #######################################################
X_train, X_test, y_train, y_test = \
    train_test_split(features, labels[-len(features):], test_size = 0.1, shuffle=False, random_state=0)
scaler = StandardScaler()
l_reg = LogisticRegression(max_iter=10000)
clf = make_pipeline(StandardScaler(), l_reg)

clf.fit(X_train, y_train)


####################### Model Running #######################################################
y_pred = clf.predict(X_test)
y_clf_prob = clf.predict_proba(X_test)
X_pred = clf.predict(X_train)
X_pred_prob = clf.predict_proba(X_train)

print("y_pred is: ", y_pred)
print('y_clf_prob is: ', y_clf_prob)

acc = accuracy_score(y_test, y_pred)
print("accuracy is: ", acc)

print("X_pred is: ", X_pred)
print('X_pred_prob is: ', X_pred_prob)

acc_X = accuracy_score(y_train, y_pred)
print("Testing accuracy is: ", acc_X)

acc_X = accuracy_score(X_train, X_pred)
print("Training accuracy is: ", acc_X)
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
joblib.dump(clf, 'log_reg_model.pkl')


