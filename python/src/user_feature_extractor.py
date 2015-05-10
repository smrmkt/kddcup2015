#!/usr/bin/env python
#-*-coding:utf-8-*-

import itertools
import os.path

from user_feature_bag import UserFeatureBag
from feature_extractor import FeatureExtractor

base_dir = os.path.dirname(__file__)


class UserFeatureExtractor(FeatureExtractor):
    def __init__(self, data_type, mode):
        log_csv_path = '{0}/../data/{1}/log_{1}.csv'.format(base_dir, data_type)
        feature_path = '{0}/../data/feature/user_feature_{1}.csv'.format(base_dir, data_type)
        FeatureExtractor.__init__(self, mode, log_csv_path, feature_path)

    def extract(self):
        tuple_iter = self._tuple_generator(self._filtered_iter)
        grouped_iter = itertools.groupby(tuple_iter, lambda x: x[0])
        bag_iter = self._bag_generator(grouped_iter)
        feature_iter = self._extract_user_features(bag_iter)
        self._save_to_file(feature_iter)
        self._log_csv.close()

    def _save_to_file(self, iter):
        with open(self._feature_path, 'w') as feature_file:
            header_written = False
            for bag in iter:
                if header_written is not True:
                    feature_file.write('enrollment_id,{0}\n'.format(
                        ','.join(bag.feature_keys)
                    ))
                    header_written = True
                for enrollment_id, feature_values in bag.feature_values_group.items():
                    feature_file.write('{0},{1}\n'.format(
                        str(enrollment_id),
                        ','.join([str(v) for v in feature_values])
                    ))

    def _extract_user_features(self, iter):
        for bag in iter:
            yield bag.extract_course_count()\
                .extract_course_access_percentage()

    def _tuple_generator(self, iter):
        for line in iter:
            user_name = (line.split(','))[1]
            yield (user_name, self._parse_line(line))

    def _bag_generator(self, iter):
        for k, g in iter:
            yield UserFeatureBag(k, [t[1] for t in g])
