import pandas as pd
import h5py
import matplotlib.pyplot as plt 

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

#Preprocessing
