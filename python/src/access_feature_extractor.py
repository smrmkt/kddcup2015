#!/usr/bin/env python
#-*-coding:utf-8-*-

import datetime
import itertools
import os.path

from access_feature_bag import AccessFeatureBag

base_dir = os.path.dirname(__file__)


class AccessFeatureExtractor():
    _log_csv_path = '{0}/../data/log_train_mini.csv'.format(base_dir)

    def __init__(self):
        log_csv = open(self._log_csv_path, 'r')
        tuple_iter = self._tuple_generator(log_csv)
        grouped_iter = itertools.groupby(tuple_iter, lambda x: x[0])
        self._bag_iter = self._bag_generator(grouped_iter)

    def extract(self):
        access_iter = self.extract_access_features(self._bag_iter)

    def extract_access_features(self, iter):
        for bag in iter:
            b = bag.extract_access_count()\
                .extract_access_days()\
                .extract_access_hours()\
                .extract_source_count()\
                .extract_event_count()
            print b.feature_keys, b.feature_values

    def _tuple_generator(self, iter):
        for line in iter:
            enrollment_id = (line.split(','))[0]
            if str.isdigit(enrollment_id):
                yield (int(enrollment_id), self._parse_line(line))

    def _bag_generator(self, iter):
        for k, g in iter:
            yield AccessFeatureBag(k, [t[1] for t in g], [], [])

    def _parse_line(self, line):
        items = line.rstrip().split(',')
        dic = {
            'user_name': items[1],
            'course_id': items[2],
            'time': datetime.datetime.strptime(items[3], '%Y-%m-%dT%H:%M:%S'),
            'source': items[4],
            'event': items[5],
            'object': items[6]
        }
        return dic


