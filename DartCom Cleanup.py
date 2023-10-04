import pandas as pd
import numpy as np
import os

columns = np.arange(2, 68)
df = pd.read_csv('Dartcom_Data/2004dbase.csv', names=columns, index_col=0)
df.index = pd.to_datetime(df.index, format='%Y%m%d%H%M', errors='coerce')
reduced = df[[53, 54, 55, 61]]
reduced.columns = ['R Hourly', 'R Daily', 'R 24', 'R Monthly']

dartcom = 'Dartcom_Data'
file_list = os.listdir(dartcom)
csv_files = [file for file in file_list if file.endswith('.csv') and '2004' not in file]

large_set = reduced

for csv in csv_files:
    file_path = os.path.join(dartcom, csv)
    with open(file_path, 'r') as file:
        max_cols = max(len(line.split(',')) for line in file)
    temp = pd.read_csv(file_path, names=np.arange(1, max_cols+2), index_col=0)
    temp.index = pd.to_datetime(temp.index, format='%Y%m%d%H%M', errors='coerce')
    temp_reduced = temp[[53, 54, 55, 61]]
    temp_reduced.columns = ['R Hourly', 'R Daily', 'R 24', 'R Monthly']
    large_set = pd.concat([large_set, temp_reduced])

large_set = large_set.sort_index()
large_set.to_csv('Dartcom_04-17_cleaned.csv')