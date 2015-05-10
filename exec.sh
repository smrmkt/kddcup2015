# feature extraction
python python/bin/extract_feature.py user train
python python/bin/extract_feature.py user test
python python/bin/extract_feature.py enrollment train
python python/bin/extract_feature.py enrollment test

# data transfer
mv python/data/feature/* r/data/feature/

# execute r script
cd r
R --vanilla --slave < src/randomforest.R
R --vanilla --slave < src/svm.R
R --vanilla --slave < src/glm.R
