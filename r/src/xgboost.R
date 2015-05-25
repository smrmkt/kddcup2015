require('data.table')
require('xgboost')
require('Matrix')

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
train.feature$enrollment_id = NULL
train.dataset$enrollment_id = NULL
## test data
test.feature.enrollment = fread('./data/feature/enrollment_feature_test.csv')
test.feature.user = fread('./data/feature/user_feature_test.csv')
test.feature = merge(test.feature.enrollment,
                     test.feature.user, by='enrollment_id')
test.enrollment_id = test.feature$enrollment_id
test.feature$enrollment_id = NULL

# sample weights
train.sumpos = sum(train.dataset$dropout==1.0)
train.sumneg = sum(train.dataset$dropout==0.0)
ratio = train.sumpos/train.sumneg
train.weights = ifelse(train.dataset$dropout==0, ratio, 1)

# xgboost
param = list('objective'= 'binary:logistic',
             'scale_pos_weight'=ratio,
             'bst:eta'=0.1,
             'bst:max_depth'=4,
             'bst:gamma'=0.3,
             'bst:subsumple'=0.5,
             'bst:colsample'=0.5,
             'bst:alpha'=1,
             'eval_metric'='auc',
             'silent' = 1,
             'nthread' = 16)
train.cv = xgb.cv(param=param,
                  sparse.model.matrix(dropout~., train.dataset),
                  label=train.truth$dropout,
                  nfold=round(1+log2(nrow(train.feature))),
                  nrounds=200)
nround = which.max(train.cv$test.auc.mean)
xgmat = xgb.DMatrix(sparse.model.matrix(dropout~., train.dataset),
                    label=train.truth$dropout,
                    weight=train.weights,
                    missing=-999.0)
train.fit = xgb.train(param, xgmat, nround)

# predict train data
train.predict = predict(train.fit, sparse.model.matrix(dropout~., train.dataset))
train.predict.b = as.numeric(train.predict > 0.5)
table(train.predict.b, train.truth$dropout)

# predict test data
test.predict = predict(train.fit, sparse.model.matrix(~., test.feature))
test.predict.out = as.data.frame(cbind(test.enrollment_id, test.predict))
setnames(test.predict.out,
         colnames(test.predict.out),
         c('enrollment_id', 'dropout'))
write.table(test.predict.out,
            './data/predict/predict.xgboost.csv', 
            sep=',', col.names=F, row.names=F, quote=F)

