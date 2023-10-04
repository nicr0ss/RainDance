import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import model_selection
import numpy as np
pd.set_option('display.max_columns', None)


rain = pd.read_csv('Austins-Bridge-rainfall-15min-Qualified.csv')
rain.set_index('dateTime', inplace=True)
rain.index = pd.to_datetime(rain.index)
rain = rain[['value']]
rain.columns = ['R 15M']
rain['R 24H SUM'] = rain['R 15M'].rolling(window=96).sum() # remember to drop NaN for regression
rain['R 1H SUM'] = rain['R 15M'].rolling(window=4).sum()
rain['R 7D_15M AVG'] = rain['R 15M'].rolling(window=672).mean()
rain['R 24H_1H AVG'] = rain['R 1H SUM'].rolling(window=96).mean()

river = pd.read_csv('Austins-Bridge-level-15min-Qualified.csv')
river.set_index('dateTime', inplace=True)
river.index = pd.to_datetime(river.index)
river = river[['value']]
river.columns = ['L 15M']
river['L 7D AVG'] = river['L 15M'].rolling(window=672).mean()
river['L 1H Change'] = river['L 15M'] - river['L 15M'].shift(periods=4)
river['L 24H_1H AVG Change'] = river['L 1H Change'].rolling(window=96).mean()


combined = rain.join(river)
'''
combined = combined.dropna()
sns.scatterplot(data=combined, x='R 24H_1H AVG', y='L 24H_1H AVG Change')
plt.show()
'''
X = combined.dropna()[['R 1H SUM', 'R 24H_1H AVG', 'L 7D AVG']]
y = combined.dropna()['L 24H_1H AVG Change']

model = linear_model.LinearRegression()
model.fit(X, y)
'''
cv = model_selection.RepeatedKFold(n_splits=10, n_repeats=3)
scores = model_selection.cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv)
scores = np.absolute(scores)
print(np.mean(scores))
'''

def my_prediction(row):
    return model.predict([row[['R 1H SUM', 'R 24H_1H AVG', 'L 7D AVG']]])[0]

def new_level(row):
    return row['Predicted Move'] + row['L 15M']

predicted = combined.copy().dropna()
predicted['Predicted Move'] = predicted.apply(my_prediction, axis=1)
predicted['Predicted Level'] = predicted.apply(new_level, axis=1)
predicted.to_csv('Austins Bridge Predictions.csv')

sns.lineplot(data=predicted[['L 15M', 'Predicted Level']])
plt.show()

print(predicted)