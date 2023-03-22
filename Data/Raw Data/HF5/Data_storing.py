import pandas as pd
import h5py
# read data
Ericback = pd.read_csv('Eric-back.csv')
Ericfront = pd.read_csv('Eric-front.csv')
Ericjacket = pd.read_csv('Eric-jacket.csv')
Keshavback = pd.read_csv('Keshav-back.csv')
Keshavfront = pd.read_csv('Keshav-front.csv')
Keshavjacket = pd.read_csv('Keshav-jacket.csv')
Mingjieback = pd.read_csv('Mingjie-back.csv')
Mingjiefront = pd.read_csv('Mingjie-Front.csv')
Mingjiejacket = pd.read_csv('Mingjie-jacket.csv')

Ericback = Ericback.drop(Ericback.columns[0], axis=1)
Ericback['Activity'] = pd.to_numeric(Ericback['Activity'], errors='coerce')
Ericfront = Ericfront.drop(Ericfront.columns[0], axis=1)
Ericfront['Activity'] = pd.to_numeric(Ericfront['Activity'], errors='coerce')
Ericjacket = Ericjacket.drop(Ericjacket.columns[0], axis=1)
Ericjacket['Activity'] = pd.to_numeric(Ericjacket['Activity'], errors='coerce')
Keshavback = Keshavback.drop(Keshavback.columns[0], axis=1)
Keshavback['Activity'] = pd.to_numeric(Keshavback['Activity'], errors='coerce')
Keshavfront = Keshavfront.drop(Keshavfront.columns[0], axis=1)
Keshavfront['Activity'] = pd.to_numeric(Keshavfront['Activity'], errors='coerce')
Keshavjacket = Keshavjacket.drop(Keshavjacket.columns[0], axis=1)
Keshavjacket['Activity'] = pd.to_numeric(Keshavjacket['Activity'], errors='coerce')
Mingjieback = Mingjieback.drop(Mingjieback.columns[0], axis=1)
Mingjieback['Activity'] = pd.to_numeric(Mingjieback['Activity'], errors='coerce')
Mingjiefront = Mingjiefront.drop(Mingjiefront.columns[0], axis=1)
Mingjiefront['Activity'] = pd.to_numeric(Mingjiefront['Activity'], errors='coerce')
Mingjiejacket = Mingjiejacket.drop(Mingjiejacket.columns[0], axis=1)
Mingjiejacket['Activity'] = pd.to_numeric(Mingjiejacket['Activity'], errors='coerce')

# print(Ericback.dtypes)
# choose indexes
E_chunks_back = [Ericback[i:i+500] for i in range(0, len(Ericback), 500)]
for i, E_chunks_back in enumerate(E_chunks_back):
    E_chunks_back.to_csv(f'E_chunk_back_{i+1}.csv', index=False)
E_chunks_front = [Ericfront[i:i+500] for i in range(0, len(Ericfront), 500)]
for i, E_chunks_front in enumerate(E_chunks_front):
    E_chunks_front.to_csv(f'E_chunk_front_{i+1}.csv', index=False)
E_chunks_jacket = [Ericjacket[i:i+500] for i in range(0, len(Ericjacket), 500)]
for i, E_chunks_jacket in enumerate(E_chunks_jacket):
    E_chunks_jacket.to_csv(f'E_chunk_jacket_{i+1}.csv', index=False)
K_chunks_back = [Keshavback[i:i+2000] for i in range(0, len(Keshavback), 2000)]
for i, K_chunks_back in enumerate(K_chunks_back):
    K_chunks_back.to_csv(f'K_chunk_back_{i+1}.csv', index=False)
K_chunks_front = [Keshavfront[i:i+2000] for i in range(0, len(Keshavfront), 2000)]
for i, K_chunks_front in enumerate(K_chunks_front):
    K_chunks_front.to_csv(f'K_chunk_front_{i+1}.csv', index=False)
K_chunks_jacket = [Keshavjacket[i:i+2000] for i in range(0, len(Keshavjacket), 2000)]
for i, K_chunks_jacket in enumerate(K_chunks_jacket):
    K_chunks_jacket.to_csv(f'E_chunk_jacket_{i+1}.csv', index=False)
M_chunks_back = [Mingjieback[i:i+2500] for i in range(0, len(Mingjieback), 2500)]
for i, M_chunks_back in enumerate(M_chunks_back):
    M_chunks_back.to_csv(f'M_chunk_back_{i+1}.csv', index=False)
M_chunks_front = [Mingjiefront[i:i+2500] for i in range(0, len(Mingjiefront), 2500)]
for i, M_chunks_front in enumerate(M_chunks_front):
    M_chunks_front.to_csv(f'M_chunk_front_{i+1}.csv', index=False)
M_chunks_jacket = [Mingjiejacket[i:i+2500] for i in range(0, len(Mingjiejacket), 2500)]
for i, M_chunks_jacket in enumerate(M_chunks_jacket):
    M_chunks_jacket.to_csv(f'M_chunk_jacket_{i+1}.csv', index=False)
# combine chunks
back_chunks = pd.concat([E_chunks_back, K_chunks_back, M_chunks_back], axis=0)
front_chunks = pd.concat([E_chunks_front, K_chunks_front, M_chunks_front], axis=0)
jacket_chunks = pd.concat([E_chunks_jacket, K_chunks_jacket, M_chunks_jacket], axis=0)
# choose data for train and test
back_train = back_chunks[:int(len(back_chunks)*0.9)]
back_test = back_chunks[int(len(back_chunks)*0.9):]
front_train = front_chunks[:int(len(front_chunks)*0.9)]
front_test = front_chunks[int(len(front_chunks)*0.9):]
jacket_train = jacket_chunks[:int(len(jacket_chunks)*0.9)]
jacket_test = jacket_chunks[int(len(jacket_chunks)*0.9):]
with h5py.File('./hdf5_GroupProject.h5', 'w') as hdf:
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
    G411 = hdf.create_group('dataset/train/back')
    for i, back_train in enumerate(back_train):
        back_train_data = f"back_train_{i}"
        dataset_back_train = G411.create_dataset(back_train_data, data=back_train)
    G412 = hdf.create_group('dataset/train/front')
    for i, front_train in enumerate(front_train):
        front_train_data = f"front_train{i}"
        dataset_front_train = G412.create_dataset(front_train_data, data=front_train)
    G413 = hdf.create_group('dataset/train/jacket')
    for i, jacket_train in enumerate(jacket_train):
        jacket_train_data = f"jacket_train{i}"
        dataset_jacket_train = G413.create_dataset(jacket_train_data, data=jacket_train)
    G421 = hdf.create_group('dataset/test/back')
    for i, back_test in enumerate(back_test):
        back_test_data = f"back_test_{i}"
        dataset_back_test = G411.create_dataset(back_test_data, data=back_test)
    G422 = hdf.create_group('dataset/test/front')
    for i, front_test in enumerate(front_test):
        front_test_data = f"front_test{i}"
        dataset_front_test = G412.create_dataset(front_test_data, data=front_test)
    G423 = hdf.create_group('dataset/test/jacket')
    for i, jacket_test in enumerate(jacket_test):
        jacket_test_data = f"jacket_test{i}"
        dataset_jacket_test = G413.create_dataset(jacket_test_data, data=jacket_test)






