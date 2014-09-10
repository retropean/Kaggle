import csv as csv 
import numpy as np

csv_file_object = csv.reader(open('data/train.csv', 'rb')) 
header = csv_file_object.next()

data=[]

for row in csv_file_object:
    data.append(row)
data = np.array(data)

#print data[0::,4] #0:: means all data
#print data[0::,2].astype(np.float)

number_passengers = np.size(data[0::,1].astype(np.float))
number_survived = np.sum(data[0::,1].astype(np.float))
proportion_survivors = number_survived / number_passengers
print 'Total amount of passengers was %s' % number_passengers
print 'Total amount of survivors %s' % number_survived
print 'Total Titanic survival rate is %s' % proportion_survivors

women_only_stats = data[0::,4] == "female" #num. of females
men_only_stats = data[0::,4] != "female" #num. of males

# Using the index from above we select the females and males separately
women_onboard = data[women_only_stats,1].astype(np.float)     
men_onboard = data[men_only_stats,1].astype(np.float)

# Then we finds the proportions of them that survived
proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)  
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard) 

print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived