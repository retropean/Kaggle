setwd("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand")

#Import train & test manipulated by Pandas to avoid doing the same work twice
train <- read.csv("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand/data/train_data-1419796230-250.csv")
test <- read.csv("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand/data/test_data-1419796230-250.csv")

library(party)
library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)
library(randomForest)

str(train)
train$season <- factor(train$season)
train$holiday <- factor(train$holiday)
train$workingday <- factor(train$workingday)
train$weather <- factor(train$weather)
train$hour <- factor(train$hour)
train$year <- factor(train$year)
train$sunindicator <- factor(train$sunindicator)
#table(train$atemp)
str(train)

str(test)
test$season <- factor(test$season)
test$holiday <- factor(test$holiday)
test$workingday <- factor(test$workingday)
test$weather <- factor(test$weather)
test$hour <- factor(test$hour)
test$year <- factor(test$year)
test$sunindicator <- factor(test$sunindicator)
#table(test$atemp)
str(test)

fit <- rpart(registered ~ season + holiday + workingday + weather + atemp + hour + year + sunindicator, data=train, method="anova")
plot(fit)
text(fit)
fancyRpartPlot(fit)

set.seed(200)
#random forest for the registered users
fit <- randomForest(as.integer(registered) ~ season + workingday + weather + atemp + hour + year + sunindicator, data=train, importance=TRUE, ntree=500)
varImpPlot(fit)
RegPrediction <- predict(fit, test, OOB=TRUE, type = "response")

#random forest for the casual users
fit <- randomForest(as.integer(casual) ~ season + workingday + weather + atemp + hour + year + sunindicator, data=train, importance=TRUE, ntree=500)
varImpPlot(fit)
CasPrediction <- predict(fit, test, OOB=TRUE, type = "response")

submit <- data.frame(datetime = test$datetime, registered = RegPrediction, casual = CasPrediction)
submit$count <- as.integer(submit$registered) + as.integer(submit$casual)
#submit <- submit[datetime, count]
submit$registered <- NULL
submit$casual <-NULL
write.csv(submit, file = "data/firstforest.csv", row.names = FALSE)
