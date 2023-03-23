import pandas as pd
import h5py
import matplotlib.pyplot as plt 

with h5py.File('alldata.h5', 'r') as hdf:
    train_data = hdf['Eric']['back']
    column_names = hdf['Eric']['back'].attrs['column_names']
    train_data_df = pd.DataFrame(train_data, columns=column_names)
    print(train_data_df.columns)


activity_data = {0: train_data_df[train_data_df['Activity'] == 0],
                 1: train_data_df[train_data_df['Activity'] == 1],
                 2: train_data_df[train_data_df['Activity'] == 2],
                 3: train_data_df[train_data_df['Activity'] == 3]}

accel_axes = ['Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)']

fig, axes = plt.subplots(4, 3, figsize=(15, 15))

for i, activity in enumerate(activity_data.keys()):
    for j, accel_axis in enumerate(accel_axes):
        axes[i][j].plot(activity_data[activity]['Time (s)'], activity_data[activity][accel_axis])
        axes[i][j].set_title(f"Activity {activity}: {accel_axis}")

plt.tight_layout()
plt.show()