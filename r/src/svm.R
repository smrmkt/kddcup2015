require('e1071')
require('data.table')

# load data
feature_train = fread('./data/feature_train.csv')
feature_test = fread('./data/feature_test.csv')
truth_train = fread('./data/truth_train.csv')
setnames(truth_train, colnames(truth_train), c('enrollment_id', 'dropout'))
data_train = merge(truth_train, feature_train, by='enrollment_id')

# randomforest model
t = proc.time()
fit.svm = svm(dropout~.,data=data_train)
proc.time()-t

# predict test data
predict.svm = predict(fit.svm, feature_test)
predict.svm.b = as.numeric(predict.svm > 0.5)
predict.svm.out = as.data.frame(
  cbind(feature_test$enrollment_id, predict.svm.b))
setnames(predict.svm.out, colnames(predict.svm.out), c('enrollment_id', 'dropout'))
write.table(predict.svm.out,
            "./data/predict.svm.out.csv", 
            sep=',', col.names=F, row.names=F, quote=F)


