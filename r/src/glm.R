require('data.table')

# load data
## train data
train.feature.enrollment = fread('./data/feature/enrollment_feature_train.csv')
train.feature.user = fread('./data/feature/user_feature_train.csv')
train.feature = merge(train.feature.enrollment,
                      train.feature.user, by='enrollment_id')
train.truth = fread('./data/feature/truth_train.csv')
train.truth = train.truth[1:nrow(train.feature),]
setnames(train.truth, colnames(train.truth), c('enrollment_id', 'dropout'))
train.dataset = merge(train.feature, train.truth, by='enrollment_id')
train.dataset$enrollment_id = NULL
## test data
test.feature.enrollment = fread('./data/feature/enrollment_feature_test.csv')
test.feature.user = fread('./data/feature/user_feature_test.csv')
test.feature = merge(test.feature.enrollment,
                     test.feature.user, by='enrollment_id')

# model
t = proc.time()
sumpos = sum(train.dataset$dropout==1.0)
sumneg = sum(train.dataset$dropout==0.0)
ratio = sumpos/sumneg
train.weights = ifelse(train.dataset$dropout==0, ratio, 1)
train.fit = glm(dropout~., data=train.dataset,
                family=binomial, weights=train.weights)
proc.time()-t

# predict test data
test.predict = predict(train.fit, test.feature, type='response')
test.predict.out = as.data.frame(cbind(test.feature$enrollment_id, test.predict))
setnames(test.predict.out,
         colnames(test.predict.out),
         c('enrollment_id', 'dropout'))
write.table(test.predict.out,
            "./data/predict/predict.glm.csv", 
            sep=',', col.names=F, row.names=F, quote=F)

