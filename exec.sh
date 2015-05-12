# args
mode=''
debug_limit=''
if [ $# == 2 ]; then
    mode=$1
    debug_limit=$2
fi

# feature extraction
python python/bin/extract_feature.py user train $mode $debug_limit
python python/bin/extract_feature.py user test $mode $debug_limit
python python/bin/extract_feature.py enrollment train $mode $debug_limit
python python/bin/extract_feature.py enrollment test $mode $debug_limit

# data transfer
cp python/data/feature/* r/data/feature/

# execute r script
cd r
#R --vanilla --slave < src/randomforest.R
#R --vanilla --slave < src/svm.R
R --vanilla --slave < src/glm.R
