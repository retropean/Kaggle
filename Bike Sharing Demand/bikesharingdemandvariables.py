import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from datetime import datetime
from datetime import timedelta
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/train.csv', header=0)
sundata = pd.read_csv('data/suntimes.csv', header=0)

#create variables for each hour of the day, year, dow, month, and date
df['time'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').time())
df['hour'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
df['year'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
df['dow'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').isoweekday())
df['month'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)
df['dateandtime'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
df['date'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'))

#create indicator for rush hour, 6 to 9am and 3 to 6pm
df['rushhour'] = np.where(((df['hour']>=6) & (df['hour'] <=9)) | ((df['hour']>=15) & (df['hour'] <=18)),1,0)

#adjust dates on sundata, drop unneccesary rows
sundata['date'] = sundata['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
sundata['sunrise'] = sundata['sunrise'].apply(lambda x: datetime.strptime(str(x), "%H%M").time())
sundata['sunset'] = sundata['sunset'].apply(lambda x: datetime.strptime(str(x), "%H%M").time())

def sunrisecombine(x):
	return (datetime.combine(x['date'], x['sunrise']))

def sunsetcombine(x):
	return (datetime.combine(x['date'], x['sunset']))	

sundata['sunrise'] = sundata.apply(sunrisecombine, axis=1)
sundata['sunset'] = sundata.apply(sunsetcombine, axis=1)

print sundata.head()
print sundata.info()

#drop unnecessary variables from sundata
sundata = sundata.drop(['month', 'day', 'year'], axis=1)

sundata['date'] = sundata['date'].apply(lambda x: datetime.strftime(x, '%m/%d/%Y'))

#merge the sundata into df
df = pd.merge(df, sundata, on='date')

#create sunindicator variable which compares sunrise and sunset to time of data and assigns a 1 if the sun is up and a 0 if it is not, with a 30 minute grace period.
df['sunindicator'] = np.where((((df['sunrise']) - (timedelta(minutes=30))) < df['dateandtime']) & (((df['sunset']) + (timedelta(minutes=30))) > df['dateandtime']) ,1,0)

#print df.mean()
#print df.describe()
print df.head()
print df.info()

#drop unnecessary variables from df
df = df.drop(['sunrise', 'sunset', 'dateandtime', 'date', 'time', 'datetime'], axis=1)

#create csv with new variables
df.to_csv('data/output.csv')

df_data = df.values

print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( df_data[0::,1::], df_data[0::,0] )

print 'Predicting...'
output = forest.predict(df_data).astype(int)

predictions_file = open("data/myfirstforest.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["Date","Survived"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'