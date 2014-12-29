setwd("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand")

#Import train & test manipulated by Pandas to avoid doing the same work twice
train <- read.csv("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand/data/train_data-1419803491-250.csv")
test <- read.csv("C:/Users/Lenovo/Desktop/Kaggle/Bike Sharing Demand/data/test_data-1419803491-250.csv")

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
train$dow <- factor(train$dow)
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
test$dow <- factor(test$dow)
#table(test$atemp)
str(test)
#aggregate(train[,"casual"],list(train$dow),mean)

fit <- rpart(registered ~ season + holiday + workingday + weather + atemp + hour + year + sunindicator, data=train, method="anova")
plot(fit)
text(fit)
fancyRpartPlot(fit)

#create Sunday variable
train$sunday[train$dow == 7] <- "1"
train$sunday[train$dow != 7] <- "0"

test$sunday[test$dow == 7] <- "1"
test$sunday[test$dpw != 7] <- "0"

#convert to factor
train$sunday <- as.factor(train$sunday)
test$sunday <- as.factor(test$sunday)

set.seed(200)
#random forest for the registered users
regfit <- randomForest(as.integer(registered) ~ sunday + season + workingday + weather + atemp + hour + year + sunindicator + holiday, data=train, importance=TRUE, ntree=500)
varImpPlot(regfit)
RegPrediction <- predict(regfit, test, OOB=TRUE, type = "response")

#random forest for the casual users
casfit <- randomForest(as.integer(casual) ~ sunday + season + workingday + weather + atemp + hour + year + sunindicator + holiday, data=train, importance=TRUE, ntree=500)
varImpPlot(casfit)
CasPrediction <- predict(casfit, test, OOB=TRUE, type = "response")

submit <- data.frame(datetime = test$datetime, registered = RegPrediction, casual = CasPrediction)
submit$count <- as.integer(submit$registered) + as.integer(submit$casual)
submit$registered <- NULL
submit$casual <-NULL
write.csv(submit, file = "data/firstforest.csv", row.names = FALSE)
