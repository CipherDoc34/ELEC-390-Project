import pandas as pd
import h5py
import random
# read data
Ericback = pd.read_csv('Eric-back.csv')
Ericfront = pd.read_csv('Eric-front.csv')
Ericjacket = pd.read_csv('Eric-jacket.csv')
Keshavback = pd.read_csv('Keshav-back.csv')
Keshavfront = pd.read_csv('Keshav-front.csv')
Keshavjacket = pd.read_csv('Keshav-jacket.csv')
Mingjieback = pd.read_csv('Mingjie-back.csv')
Mingjiefront = pd.read_csv('Mingjie-front.csv')
Mingjiejacket = pd.read_csv('Mingjie-jacket.csv')

def toNum(df):
    activity = []
    for i in range(len(df['Activity'])):  
        if(df['Activity'][i] == "Transition"):
            activity.append(0)
        if(df['Activity'][i] == "Standing"):
            activity.append(1)
        if(df['Activity'][i] == "Jumping"):
            activity.append(2)
        if(df['Activity'][i] == "Walking"):
            activity.append(3)
    df = df.drop(columns=["Activity"])
    df['Activity'] = activity
    return df

def shuffle(df):
    lis = [df[i:i+500] for i in range(0, len(df), 500)]
    random.shuffle(lis)
    return pd.concat(lis)

Ericback = toNum(Ericback)
Ericfront = toNum(Ericfront)
Ericjacket = toNum(Ericjacket)
Keshavback = toNum(Keshavback)
Keshavfront = toNum(Keshavfront)
Keshavjacket = toNum(Keshavjacket)
Mingjieback = toNum(Mingjieback)
Mingjiefront = toNum(Mingjiefront)
Mingjiejacket = toNum(Mingjiejacket)

# choose indexes
E_chunks_back = shuffle(Ericback)
E_chunks_front = shuffle(Ericfront)
E_chunks_jacket = shuffle(Ericjacket)
K_chunks_back = shuffle(Keshavback)
K_chunks_front = shuffle(Keshavfront)
K_chunks_jacket = shuffle(Keshavjacket)
M_chunks_back = shuffle(Mingjieback)
M_chunks_front = shuffle(Mingjiefront)
M_chunks_jacket = shuffle(Mingjiejacket)

# combine chunks
chunks = [E_chunks_back, K_chunks_back, M_chunks_back,
         E_chunks_front, K_chunks_front, M_chunks_front,
         E_chunks_jacket, K_chunks_jacket, M_chunks_jacket]
random.shuffle(chunks)
alldata = pd.concat(chunks, axis=0)

# choose data for train and test
train_data = alldata[:int(len(alldata)*0.9)]
test_data = train_data = alldata[int(len(alldata)*0.9):]

with h5py.File('./alldata.h5', 'w') as hdf:
    G1 = hdf.create_group('Eric')
    G1.create_dataset('back', data=Ericback)
    G1.create_dataset('front', data=Ericfront)
    G1.create_dataset('jacket', data=Ericjacket)
    G2 = hdf.create_group('Keshav')
    G2.create_dataset('back', data=Ericback)
    G2.create_dataset('front', data=Ericfront)
    G2.create_dataset('jacket', data=Ericjacket)
    G3 = hdf.create_group('Mingjie')
    G3.create_dataset('back', data=Ericback)
    G3.create_dataset('front', data=Ericfront)
    G3.create_dataset('jacket', data=Ericjacket)
    G41 = hdf.create_group('dataset/train')
    G41.create_dataset("trainData", data=train_data)
    G42 = hdf.create_group('dataset/test')
    G42.create_dataset("testData", data=test_data)