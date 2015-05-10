#!/usr/bin/env python
#-*-coding:utf-8-*-

import datetime
import itertools
import os.path

from enrollment_feature_bag import EnrollmentFeatureBag
from feature_extractor import FeatureExtractor

base_dir = os.path.dirname(__file__)


class EnrollmentFeatureExtractor(FeatureExtractor):
    def __init__(self, data_type, mode):
        log_csv_path = '{0}/../data/{1}/log_{1}.csv'.format(base_dir, data_type)
        feature_path = '{0}/../data/feature/feature_{1}.csv'.format(base_dir, data_type)
        FeatureExtractor.__init__(self, mode, log_csv_path, feature_path)

    def extract(self):
        tuple_iter = self._tuple_generator(self._filtered_iter)
        grouped_iter = itertools.groupby(tuple_iter, lambda x: x[0])
        bag_iter = self._bag_generator(grouped_iter)
        access_iter = self.extract_enrollment_features(bag_iter)
        self._save_to_file(access_iter)
        self._log_csv.close()

    def extract_enrollment_features(self, iter):
        for bag in iter:
            yield bag.extract_access_count()\
                .extract_access_days()\
                .extract_access_hours()\
                .extract_source_count()\
                .extract_event_count()

    def _tuple_generator(self, iter):
        for line in iter:
            enrollment_id = (line.split(','))[0]
            if str.isdigit(enrollment_id):
                yield (int(enrollment_id), self._parse_line(line))

    def _bag_generator(self, iter):
        for k, g in iter:
            yield EnrollmentFeatureBag(k, [t[1] for t in g], [], [])
