import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/train.csv', header=0)
sundata = pd.read_csv('data/suntimes.csv', header=0)

#create variable for each hour of the day
df['hour'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)

#create variable for the year
df['year'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)

#create variable for dow
df['dow'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').isoweekday())

#create variable for month
df['month'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)

#create variable for date
df['date'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'))

#create indicator for rush hour
df['rushhour'] = df['hour'].map({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 1, 16: 1, 17: 1, 18: 1, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0})

#adjust date on sundata
sundata['date'] = sundata['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%m/%d/%Y'))
#drop unnecessary rows from sundata
sundata = sundata.drop(['month', 'day', 'year'], axis=1)

#merge the sundata into df
df = pd.merge(df, sundata, on='date')

#print sundata.describe()
#print sundata.head()
print sundata.info()

#print df.mean()
print df.describe()
print df.head()
print df.info()

#create csv with new variables
df.to_csv('data/output.csv')