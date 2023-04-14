Github - https://github.com/CipherDoc34/ELEC-390-Project
390 Final Project 
By:
Keshav Aggarwal (20231278, 19ka47@queensu.ca)
Eric Ryu (20232970, 20jkr@queensu.ca)
Mingjie (Stephen) Gao (20179479, 19mg8@queensu.ca)

Files included:
DataLabeling.py - took the raw phyphox data and labeled it based on the controlled tests that were performed by each group member
DataTohdf5.py - took the labeled CSVs and put it into hdf5 format
alldata.h5 - contains the data in the formatted file structure
Steps3to6.py - uses alldata.h5 to do: Data Visualization, Pre-processing, Feature Extraction, Model Training, and Model Prediction on Training data and Testing data
AppWithLiveData.py - The Final app that was developed for the project
lof_reg_model.pkl - joblib pickle file that contains the trained model
preprocessing_features.py - the class that preprocessess and extracts features of new Phyphox data
preprocessing_features_bonus.py - the class that preprocessess and extracts features of live Phyphox data
preprocessing_features.pkl - pickle dump of preprocessing_features.py
preprocessing_features_bonus.pkl - pickle dump of preprocessing_features_bonus.py
README.txt - this file

How to run
run "python AppWithLiveData.py" in terminal to run the app


Controlled data collection test
test: 30 seconds - standing, 5 seconds - blank, 30seconds  - walking, 5 seconds - blank, 30 seconds - jumping : 1:40 - 100 seconds

Variations:
Front Pocket
Back Pocket
Jacket Pocket


HDF5 format
alldata.h5/
├── dataset/
│   ├── Train
│   └── Test
├── Keshav (raw data)/
│   ├── back
│   ├── front
│   └── jacket
├── Eric (raw data)/
│   ├── back
│   ├── front
│   └── jacket
└── Mingjie (raw data)/
    ├── back
    ├── front
    └── jacket