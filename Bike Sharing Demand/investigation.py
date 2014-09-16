import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/train.csv', header=0)
print df.info()
print df.describe()

#Turn datetime into time: hour, rushhour/nonrushhour, dow, month