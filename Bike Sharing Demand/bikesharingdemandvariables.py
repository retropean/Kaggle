import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/train.csv', header=0)

#Create variable for each hour of the day
df['hour'] = df['datetime']
df['hour'] = df.hour.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)

#Create variable for DOW
df['dow'] = df['datetime']
df['dow'] = df.dow.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').isoweekday())

#Create variable for Month
df['month'] = df['datetime']
df['month'] = df.month.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)

#Create indicator for Rush Hour


#print df.mean()
print df.describe()
print df.head()
#print df.info()