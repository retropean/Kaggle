import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from datetime import datetime
from datetime import timedelta
from sklearn.ensemble import RandomForestClassifier

#MANIPULATING SUNTIMES.CSV
def sunrisecombine(x):
	return (datetime.combine(x['date'], x['sunrise']))

def sunsetcombine(x):
	return (datetime.combine(x['date'], x['sunset']))	
	
sundata = pd.read_csv('data/suntimes.csv', header=0)
#adjust dates on sundata, drop unneccesary rows
sundata['date'] = sundata['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
sundata['sunrise'] = sundata['sunrise'].apply(lambda x: datetime.strptime(str(x), "%H%M").time())
sundata['sunset'] = sundata['sunset'].apply(lambda x: datetime.strptime(str(x), "%H%M").time())
sundata['sunrise'] = sundata.apply(sunrisecombine, axis=1)
sundata['sunset'] = sundata.apply(sunsetcombine, axis=1)
#drop unnecessary variables from sundata
sundata = sundata.drop(['month', 'day', 'year'], axis=1)
sundata['date'] = sundata['date'].apply(lambda x: datetime.strftime(x, '%m/%d/%Y'))

#################
#CREATE TRAIN_DF#
#################
train_df = pd.read_csv('data/train.csv', header=0)

#create variables for each hour of the day, year, dow, month, and date
train_df['time'] = train_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').time())
train_df['hour'] = train_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
train_df['year'] = train_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
train_df['dow'] = train_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').isoweekday())
train_df['month'] = train_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)
train_df['dateandtime'] = train_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
train_df['date'] = train_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'))
#create indicator for rush hour, 6 to 9am and 3 to 6pm
train_df['rushhour'] = np.where(((train_df['hour']>=6) & (train_df['hour'] <=9)) | ((train_df['hour']>=15) & (train_df['hour'] <=18)),1,0)

#MERGE SUNDATA ON TRAIN_DF
train_df = pd.merge(train_df, sundata, on='date')
#create sunindicator variable which compares sunrise and sunset to time of data and assigns a 1 if the sun is up and a 0 if it is not, with a 30 minute grace period.
train_df['sunindicator'] = np.where((((train_df['sunrise']) - (timedelta(minutes=30))) < train_df['dateandtime']) & (((train_df['sunset']) + (timedelta(minutes=30))) > train_df['dateandtime']) ,1,0)

print 'train_df info'
print train_df.head()
print train_df.info()
print train_df.describe()

#DROP UNNECESSARY VARIABLES FROM TRAIN_DF
dateid = train_df['datetime'].values
train_df = train_df.drop(['sunrise', 'sunset', 'date', 'datetime', 'dateandtime','time','temp','dow','month','count','rushhour','windspeed','humidity'], axis=1)

'''
regtrain_df = train_df.copy(deep=True)
regtrain_df = regtrain_df.drop(['casual'])
castrain_df = train_df.copy(deep=True)
print 'castrain infoooooo'
print castrain_df.info()
castrain_df = castrain_df.drop('registered')
'''

################
#CREATE TEST_DF#
################
test_df = pd.read_csv('data/test.csv', header=0)

#create variables for each hour of the day, year, dow, month, and date
test_df['time'] = test_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').time())
test_df['hour'] = test_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)
test_df['year'] = test_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
test_df['dow'] = test_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').isoweekday())
test_df['month'] = test_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)
test_df['dateandtime'] = test_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
test_df['date'] = test_df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y'))
#create indicator for rush hour, 6 to 9am and 3 to 6pm
test_df['rushhour'] = np.where(((test_df['hour']>=6) & (test_df['hour'] <=9)) | ((test_df['hour']>=15) & (test_df['hour'] <=18)),1,0)

#MERGE SUNDATA ON TEST_DF
test_df = pd.merge(test_df, sundata, on='date')
#create sunindicator variable which compares sunrise and sunset to time of data and assigns a 1 if the sun is up and a 0 if it is not, with a 30 minute grace period.
test_df['sunindicator'] = np.where((((test_df['sunrise']) - (timedelta(minutes=30))) < test_df['dateandtime']) & (((test_df['sunset']) + (timedelta(minutes=30))) > test_df['dateandtime']) ,1,0)

print 'test_df info'
print test_df.head()
print test_df.info()
print test_df.describe()

#DROP UNNECESSARY VARIABLES FROM TEST_DF
dateid = test_df['datetime'].values
test_df = test_df.drop(['sunrise', 'sunset', 'date', 'datetime', 'dateandtime','time','temp','dow','month','rushhour','windspeed','humidity'], axis=1)
#maybe convert time to an int

#create csv with new variables
train_df.to_csv('data/output.csv')
train_df = train_df[['registered','casual','season','holiday','workingday','weather','atemp','hour','year','sunindicator']]
train_data = train_df.values
test_data = test_df.values

train_df.to_csv('data/train_data.csv')
test_df.to_csv('data/test_data.csv')

print 'Training...'
registeredforest = RandomForestClassifier(n_estimators=11, max_features=None)
casualforest = RandomForestClassifier(n_estimators=11, max_features=None)
#sheet[rows,columns],on which variable[rows,columns]
registeredforest = registeredforest.fit(train_data[0::,2::], train_data[0::,0])
casualforest = casualforest.fit(train_data[0::,2::], train_data[0::,1])
print 'Predicting...'
totaloutput = (casualforest.predict(test_data).astype(int))+(registeredforest.predict(test_data).astype(int))
print 'Writing...'
predictions_file = open("data/mysubmission.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["datetime","count"])
open_file_object.writerows(zip(dateid, totaloutput))
predictions_file.close()
print 'Done.'
