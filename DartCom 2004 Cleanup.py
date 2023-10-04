import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

columns = np.arange(2, 68)
twoK4 = pd.read_csv('Dartcom_Data/2004dbase.csv', names=columns, index_col=0)
twoK4.index = pd.to_datetime(twoK4.index, format='%Y%m%d%H%M', errors='coerce')
reduced = twoK4[[53, 54]]
reduced.columns = ['R Daily', 'R Hourly']

plt.scatter(reduced.index, reduced['R Daily'])
plt.scatter(reduced.index, reduced['R Hourly'])
