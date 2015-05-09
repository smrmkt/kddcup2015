#!/usr/bin/env python
#-*-coding:utf-8-*-

import datetime
import itertools
import os.path

from access_feature_bag import AccessFeatureBag

base_dir = os.path.dirname(__file__)


class AccessFeatureExtractor():
    _log_csv_path = '{0}/../data/train/log_train.csv'.format(base_dir)
    _feature_path = '{0}/../data/feature/feature.csv'.format(base_dir)

    def __init__(self):
        log_csv = open(self._log_csv_path, 'r')
        tuple_iter = self._tuple_generator(log_csv)
        grouped_iter = itertools.groupby(tuple_iter, lambda x: x[0])
        self._bag_iter = self._bag_generator(grouped_iter)

    def extract(self):
        access_iter = self.extract_access_features(self._bag_iter)
        self._save_to_file(access_iter)

    def _save_to_file(self, iter):
        with open(self._feature_path, 'w') as feature_file:
            header_written = False
            for bag in iter:
                if header_written is not True:
                    feature_file.write('enrollment_id,{0}\n'.format(
                        ','.join(bag.feature_keys)
                    ))
                    header_written = True
                feature_file.write('{0},{1}\n'.format(
                    str(bag.enrollment_id),
                    ','.join([str(v)for v in bag.feature_values])
                ))

    def extract_access_features(self, iter):
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


