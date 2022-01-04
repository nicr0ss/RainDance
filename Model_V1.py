#mass import
import pandas as pd
import urllib.request
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn import linear_model
pd.options.display.max_rows = 999

#for getting the date 4 days ago
daydif = str(datetime.today() - timedelta(days=5))
dayref = str(daydif[0:10])
today = str(datetime.today().strftime('%Y-%m-%d'))

#for retrieving the data from the APIs
link = ["https://environment.data.gov.uk/flood-monitoring/id/stations/46160/readings?since=",dayref, "&_sorted&parameter=rainfall"]
final = ""
final = final.join(link)
#print(final)
web = urllib.request.Request(final)
response = urllib.request.urlopen(web)
the_page = response.read()
jason = json.loads(the_page)
link1 = ["http://environment.data.gov.uk/flood-monitoring/id/measures/46126-level-stage-i-15_min-m/readings?since=",dayref]
final1 = ""
final1 = final1.join(link1)
#print(final1)
web1 = urllib.request.Request(final1)
response1 = urllib.request.urlopen(web1)
the_page1 = response1.read()
jason1 = json.loads(the_page1)

#creates dataframes for each API
df1 = pd.DataFrame(jason1["items"])
df1 = df1.sort_values('dateTime', ascending = True)
df = pd.DataFrame(jason["items"])
df = df.sort_values('dateTime', ascending = True)

#merged table containing level and fall, plots a graph
a = pd.merge(df, df1, on = 'dateTime', how = 'left')
b = a[['dateTime', 'value_x', 'value_y']].copy()
b = b.rename(columns = {"dateTime" : "Date/Time", "value_x" : "Rainfall", "value_y" : "River Level"})
#plt.plot(b['Date/Time'],b['River Level'],label = 'River Level')
#plt.plot(b['Date/Time'],b['Rainfall'], label = 'Rainfall')
#plt.title('River Dart Rainfall against River Level')
#plt.locator_params(axis = 'Date/Time', nbins = 10)
#plt.xticks(rotation = 'vertical')
#ax = plt.gca()
#ax.set_xticks(ax.get_xticks()[::48])
#least_recent_date = b['Date/Time'].min()
#recent_date = b['Date/Time'].max()
#plt.plot([least_recent_date, recent_date], [0.35, 0.35], label = 'Scrape')
#plt.plot([least_recent_date, recent_date], [0.5, 0.5], label = 'Low')
#plt.plot([least_recent_date, recent_date], [0.74, 0.74], label = 'Medium')
#plt.plot([least_recent_date, recent_date], [1.1, 1.1], label = 'High')
#plt.plot([least_recent_date, recent_date], [1.25, 1.25], label = 'Huge')
#plt.legend(loc = 'upper right')
#plt.show()

#Calculates hourly results
c = b[['Rainfall', 'River Level']]
d = c['River Level'].groupby(c.index//4).mean()
d = d.diff()
e = c.groupby(c.index//4)['Rainfall'].sum()
hourly = pd.concat([d, e], axis = 1)
drip = hourly['Rainfall'].max()
drip = int(drip * 10)
calc = []
tester = pd.DataFrame()
for i in range (0, drip+1):
  x = i/10
  s = hourly.Rainfall.eq(x)
  out = pd.DataFrame()
  out['River'] = hourly.loc[s | s.shift(1, axis = 0) | s.shift(2, axis = 0), 'River Level']
  runner = len(out)
  out['Rain'] = x
  tester = pd.concat([tester, out])
tester = tester.dropna()

#Machine learning : Linear Regression
reg = linear_model.LinearRegression()
reg = reg.fit(tester[['Rain']], tester.River)

#Testing with user input
#currentlevel = float(input('Please enter the current river level :'))
#ran1 = float(input('Please enter the first forecast :'))
#ran2 = float(input('Please enter the second forecast :'))
#ran3 = float(input('Please enter the third forecast :'))
#ran1 = currentlevel + reg.predict([[ran1]])
#ran2 = ran1 + reg.predict([[ran2]])
#ran3 = ran2 + reg.predict([[ran3]])
#print(ran1, ran2, ran3)

#Producing a graph of the regression
plt.scatter(tester['Rain'], tester['River'], color = 'Blue', marker = '+')
plt.plot(tester['Rain'], reg.predict(tester[['Rain']]), color = 'Red')
plt.show()

#Producing an example prediction
pred = pd.DataFrame()
#print(pred)
end = len(b.index)
for i in range(1, end):
  prod = pd.DataFrame()
#print(b)
for row in b.itertuples():
  temp = pd.DataFrame()
  temp['RDelta'] = reg.predict([[row.Rainfall]])
  temp['Rainfall'] = row.Rainfall
  pred = pd.concat([pred, temp])
endriver = pd.DataFrame()
riverstart = b['River Level'].iloc[0]
for row in pred.itertuples():
  rtemp = pd.DataFrame({'RPred': [riverstart]})
  endriver = pd.concat([endriver, rtemp], ignore_index = True)
  riverstart = riverstart + row.RDelta
#print(endriver)

#Producing a dataframe with the prediction and all other data together
fin = pd.merge(b, endriver, left_index = True, right_index = True)
print(fin)

#Plotting a graph of expected riverlevel and the actual river level
plt.plot(fin['Date/Time'],fin['River Level'],label = 'River Level')
plt.plot(fin['Date/Time'],fin['Rainfall'], label = 'Rainfall')
plt.plot(fin['Date/Time'],fin['RPred'], label = 'Predicted')
plt.locator_params(axis = 'Date/Time', nbins = 10)
plt.xticks(rotation = 'vertical')
ax = plt.gca()
ax.set_xticks(ax.get_xticks()[::48])
plt.show()





