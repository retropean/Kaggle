import numpy as np
import pandas as pd
import pylab as P

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

#Convert gender to 0 and 1
df['Gender'] = df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
#df['EmbarkedFix'] = df['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)
#print df.head()



median_ages = np.zeros((2,3))
#print median_ages

for i in range(0, 2):
    for j in range(0, 3):
        median_ages[i,j] = df[(df['Gender'] == i) & \
                              (df['Pclass'] == j+1)]['Age'].dropna().median()
 
#print median_ages
df['AgeFill'] = df['Age']

for i in range(0, 2):
    for j in range(0, 3):
        df.loc[ (df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j+1),'AgeFill'] = median_ages[i,j]

df['AgeIsNull'] = pd.isnull(df.Age).astype(int)

print df[ df['Age'].isnull() ][['Gender','Pclass','Age','AgeFill','AgeIsNull']].head(10)

print df.describe()