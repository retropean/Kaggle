setwd("~/GitHub/Kaggle/Titanic-R")
train <- read.csv("~/GitHub/Kaggle/Titanic-R/train.csv")
test <- read.csv("~/GitHub/Kaggle/Titanic-R/test.csv")

str(train)
table(train$Survived)
prop.table(table(train$Survived))

test$Survived <- rep(0, 418)

submit <- data.frame(PassengerId = test$PassengerId, Survived = test$Survived)
write.csv(submit, file = "theyallperish.csv", row.names = FALSE)

summary(train$Sex)

prop.table(table(train$Sex, train$Survived))
#proportions in the 1st dimension stands for the rows, 2 would give you column proportions)
prop.table(table(train$Sex, train$Survived),1)

test$Survived <- 0
test$Survived[test$Sex == 'female'] <- 1

summary(train$Age)

train$Child <- 0
train$Child[train$Age < 18] <- 1

aggregate(Survived ~ Child + Sex, data=train, FUN=sum)
aggregate(Survived ~ Child + Sex, data=train, FUN=length)
aggregate(Survived ~ Child + Sex, data=train, FUN=function(x) {sum(x)/length(x)})

hist(train$Fare)
summary(train$Fare)

train$Fare2 <- '30+'
train$Fare2[train$Fare < 30 & train$Fare >= 20] <- '20-30'
train$Fare2[train$Fare < 20 & train$Fare >= 10] <- '10-20'
train$Fare2[train$Fare < 10] <- '<10'

aggregate(Survived ~ Fare2 + Pclass + Sex, data=train, FUN=function(x) {sum(x)/length(x)})

test$Survived <- 0
test$Survived[test$Sex == 'female'] <- 1
test$Survived[test$Sex == 'female' & test$Pclass == 3 & test$Fare >= 20] <- 0

submit <- data.frame(PassengerId = test$PassengerId, Survived = test$Survived)
write.csv(submit, file = "theyallperish.csv", row.names = FALSE)