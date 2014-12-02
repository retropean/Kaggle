import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from datetime import datetime
from datetime import timedelta
from sklearn.ensemble import RandomForestClassifier

train_df = pd.read_csv('data/train.csv', header=0)
train_df.columns = ['id','time last','quantity','volumes','time','don']
train_df = train_df[['don','id','time last','quantity','volumes','time']]
train_df = train_df.drop(['id'], axis=1)

'''
id = patient ID
time last = months since last donation
quantity = number of donations
volumes = total volume donated (c.c.)
time = months since first donation
don = made donation in march 2007
'''

test_df = pd.read_csv('data/test.csv', header=0)
test_df.columns = ['id','time last','quantity','volumes','time']
id = test_df['id'].values
test_df = test_df.drop(['id'], axis=1)
print train_df.describe
train_data = train_df.values
test_data = test_df.values

print 'Training...'
forest = RandomForestClassifier(n_estimators=1000, max_features=None)
forest = forest.fit(train_data[0::,1::], train_data[0::,0])
print 'Predicting...'
output = forest.predict(test_data).astype(float)
print 'Writing...'
predictions_file = open("data/mysubmission.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["","Made Donation in March 2007"])
open_file_object.writerows(zip(id, output))
predictions_file.close()
print 'Done.'
