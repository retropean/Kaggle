import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/train.csv', header=0)

#Create variable for each hour of the day
df['hour'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').hour)

#Create variable for DOW
df['dow'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').isoweekday())

#Create variable for Month
df['month'] = df.datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)

#Create indicator for Rush Hour
df['rushhour'] = df['hour'].map({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 1, 16: 1, 17: 1, 18: 1, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0})

#print df.mean()
print df.describe()
print df.head()
#print df.info()