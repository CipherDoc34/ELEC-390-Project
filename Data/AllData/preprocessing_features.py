# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 22:49:45 2023

@author: Keshav
"""

import pandas as pd
import dill as pickle
import numpy as np

class preprocessing_features:
    def __init__(self, X):
        self.X = X
        self.features = self.features()
    def features(self):
        X = self.X
        X = X.iloc[:, 1:-1]
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
        def SplitFeature(df):
            return df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]
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
        return features

with open('preprocessing_features.pkl', 'wb') as file:
        pickle.dump(preprocessing_features, file)