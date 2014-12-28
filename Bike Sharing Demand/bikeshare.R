setwd("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand")

#Import train & test manipulated by Pandas to avoid doing the same work twice
train <- read.csv("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand/data/train_data-1419791190-250.csv")
test <- read.csv("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand/data/test_data-1419791190-250.csv")

library(party)
library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)
library(randomForest)

