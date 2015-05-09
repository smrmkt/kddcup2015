require('data.table')

# load data
feature_train = fread('./data/feature_train.csv')
feature_test = fread('./data/feature_test.csv')
truth_train = fread('./data/truth_train.csv')
setnames(truth_train, colnames(truth_train), c('enrollment_id', 'dropout'))
data_train = merge(truth_train, feature_train, by='enrollment_id')

# randomforest model
t = proc.time()
fit.glm = glm(dropout~.,data=data_train, family=binomial)
proc.time()-t

# predict test data
predict.glm = predict(fit.glm, feature_test)
predict.glm.b = as.numeric(predict.glm > 0.5)
predict.glm.out = as.data.frame(
  cbind(feature_test$enrollment_id, predict.glm.b))
setnames(predict.glm.out, colnames(predict.glm.out), c('enrollment_id', 'dropout'))
write.table(predict.glm.out,
            "./data/predict.glm.out.csv", 
            sep=',', col.names=F, row.names=F, quote=F)



