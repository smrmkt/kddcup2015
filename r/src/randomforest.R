require('randomForest')
require('data.table')
require('pforeach')

# load data
feature_train = fread('./data/feature_train.csv')
feature_test = fread('./data/feature_test.csv')
truth_train = fread('./data/truth_train.csv')
setnames(truth_train, colnames(truth_train), c('enrollment_id', 'dropout'))
data_train = merge(truth_train, feature_train, by='enrollment_id')

# randomforest model
t = proc.time()
fit.rf = randomForest(dropout~., data=data_train, ntree=300)
proc.time()-t

# predict test data
predict.rf = predict(fit.rf, feature_test)
predict.rf.b = as.numeric(predict.rf > 0.5)
predict.rf.out = as.data.frame(
  cbind(feature_test$enrollment_id, predict.rf.b))
setnames(predict.rf.out, colnames(predict.rf.out), c('enrollment_id', 'dropout'))
write.table(predict.rf.out,
            "./data/predict.rf.out.csv", 
            sep=',', col.names=F, row.names=F, quote=F)

