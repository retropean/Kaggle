setwd("~/GitHub/Kaggle/Titanic-R")
train <- read.csv("~/GitHub/Kaggle/Titanic-R/train.csv")
test <- read.csv("~/GitHub/Kaggle/Titanic-R/test.csv")

str(train)
table(train$Survived)
prop.table(table(train$Survived))

test$Survived <- rep(0, 418)

submit <- data.frame(PassengerId = test$PassengerId, Survived = test$Survived)
write.csv(submit, file = "theyallperish.csv", row.names = FALSE)