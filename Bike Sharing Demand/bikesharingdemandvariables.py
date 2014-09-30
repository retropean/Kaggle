import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/train.csv', header=0)
sundata = pd.read_csv('data/suntimes.csv', header=0)

#create variables for each hour of the day, year, dow, month, and date
df['time'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').time())
df['hour'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
df['year'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
df['dow'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').isoweekday())
df['month'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)
df['date'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'))

#create indicator for rush hour, 6 to 9am and 3 to 6pm
df['rushhour'] = np.where(((df['hour']>=6) & (df['hour'] <=9)) | ((df['hour']>=15) & (df['hour'] <=18)),1,0)

#adjust date on sundata, drop unneccesary rows
sundata['date'] = sundata['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%m/%d/%Y'))

sundata['sunrise'] = sundata['sunrise'].apply(lambda x: datetime.strptime(str(x), "%H%M").time())
sundata['sunset'] = sundata['sunset'].apply(lambda x: datetime.strptime(str(x), "%H%M").time())
#sundata['sunset'] = (sundata['sunset'],sundata['date']).apply(lambda x,y: datetime.combine(x, y))
sundata = sundata.drop(['month', 'day', 'year'], axis=1)

#merge the sundata into df
df = pd.merge(df, sundata, on='date')

#df['sunindicator'] = np.where((((df['sunrise']) - (datetime.timedelta(minutes=30))) < df['time']) & (df['sunset']>df['time']) ,1,0)

#print sundata.describe()
#print sundata.head()
print sundata.info()

#print df.mean()
print df.describe()
print df.head()
print df.info()

#create csv with new variables
df.to_csv('data/output.csv')