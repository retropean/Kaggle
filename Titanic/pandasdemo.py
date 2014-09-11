import numpy as np
import pandas as pd
import pylab as P
import csv as csv
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/train.csv', header=0)
#print df.info()
#print df.describe()

#print df['Age'][0:10]
#print df['Age'].mean()

#Print sex, class and age.
#print df[ ['Sex', 'Pclass', 'Age'] ]

#Print all over 60
#print df[df['Age'] >60]

#Print Sex, Class, Age, and Survived for all over 60
#print df[df['Age'] > 60][['Sex', 'Pclass', 'Age', 'Survived']]

#Count number of males in each class
#for i in range(1,4):
#	print i, len(df[(df['Sex'] == 'male') & (df['Pclass'] ==i) ])

#Create histogram
#df['Age'].dropna().hist(bins=16, range=(0,80), alpha = .5)
#P.show()

#CLEANING THE DATA
#Convert gender to 0 and 1
df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
#df['EmbarkedFix'] = df['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)

#find median ages by class.
median_ages = np.zeros((2,3))

for i in range(0, 2):
    for j in range(0, 3):
        median_ages[i,j] = df[(df['Gender'] == i) & \
                              (df['Pclass'] == j+1)]['Age'].dropna().median()
 
#print median_ages
df['AgeFill'] = df['Age']

#add median age by class to those who are missing age
for i in range(0, 2):
    for j in range(0, 3):
        df.loc[ (df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j+1),'AgeFill'] = median_ages[i,j]

#indicator for rows originally without the age.
df['AgeIsNull'] = pd.isnull(df.Age).astype(int)

#print df[ df['Age'].isnull() ][['Gender','Pclass','Age','AgeFill','AgeIsNull']].head(10)

#print df.describe()

#FEATURE ENGINEERING
#Create family size 
df['FamilySize'] = df['SibSp'] + df['Parch']
#Age*Class multiplier
df['Age*Class'] = df['AgeFill'] * df['Pclass']

print df.dtypes[df.dtypes.map(lambda x: x=='object')]

df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked', 'Age'], axis=1) 

train_data = df.values

