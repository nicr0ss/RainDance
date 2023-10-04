import pandas as pd
import seaborn as sns
import random
import matplotlib.pyplot as plt

predictions = pd.read_csv('Austins Bridge Predictions.csv')
predictions_levels = predictions[['L 15M', 'Predicted Level']]

# random weeks
num_weeks = 4
weeks = []
for i in range(num_weeks):
    start = random.randint(0,len(predictions)-268)
    weeks += [predictions.iloc[start:start+268].copy()]

for week in weeks:
    levels = [week.iloc[0]['L 15M']]
    for index, row in week.iterrows():
        levels += [levels[-1] + row['Predicted Move']]
    week['Forward Level'] = levels[:-1]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10,8))
sns.lineplot(data=weeks[0][['L 15M', 'Forward Level']], ax=ax1)
sns.lineplot(data=weeks[1][['L 15M', 'Forward Level']], ax=ax2)
sns.lineplot(data=weeks[2][['L 15M', 'Forward Level']], ax=ax3)
sns.lineplot(data=weeks[3][['L 15M', 'Forward Level']], ax=ax4)
plt.tight_layout()
plt.show()