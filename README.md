# ELEC-390-Project
By:
Keshav Aggarwal (20231278, 19ka47@queensu.ca)
Eric Ryu (20232970, 20jkr@queensu.ca)
Mingjie (Stephen) Gao (20179479, 19mg8@queensu.ca)

## Files included:
`DataLabeling.py` - took the raw `Phyphox` data and labeled it based on the controlled tests that were performed by each group member <br />
`DataTohdf5.py` - took the labeled `CSV`s and put it into `hdf5` format <br />
`alldata.h5` - contains the data in the formatted file structure <br />
`Steps3to6.py` - uses `alldata.h5` to do: Data Visualization, Pre-processing, Feature Extraction, Model Training, and Model Prediction on Training data and Testing data <br />
`AppWithLiveData.py` - The Final app that was developed for the project <br />
`lof_reg_model.pkl` - joblib pickle file that contains the trained model <br />
`preprocessing_features.py` - the class that preprocessess and extracts features of new `Phyphox` data <br />
`preprocessing_features_bonus.py` - the class that preprocessess and extracts features of live `Phyphox` data <br />
`preprocessing_features.pkl` - pickle dump of `preprocessing_features.py` <br />
`preprocessing_features_bonus.pkl` - pickle dump of `preprocessing_features_bonus.py` <br />
`README.txt` - this file <br />

## How to run:
run `"python AppWithLiveData.py"` in terminal to run the app <br />


## Controlled data collection test
Process: 30 seconds - standing, 5 seconds - blank, 30seconds  - walking, 5 seconds - blank, 30 seconds - jumping : 1:40 - 100 seconds <br />

### Variations:
 - Front Pocket
 - Back Pocket
 - Jacket Pocket


## HDF5 format
alldata.h5/ <br />
├── dataset/ <br />
│   ├── Train <br />
│   └── Test <br />
├── Keshav (raw data)/ <br />
│   ├── back <br />
│   ├── front <br />
│   └── jacket <br />
├── Eric (raw data)/ <br />
│   ├── back <br />
│   ├── front <br />
│   └── jacket <br />
└── Mingjie (raw data)/ <br />
    ├── back <br />
    ├── front <br />
    └── jacket <br />
