#!/usr/bin/env python
#-*-coding:utf-8-*-

import datetime
import itertools
import os.path

from enrollment_feature_bag import EnrollmentFeatureBag

base_dir = os.path.dirname(__file__)


class FeatureExtractor():

    _DEBUG_LIMIT = 1000

    def __init__(self, mode, log_csv_path, feature_path):
        self._log_csv_path = log_csv_path
        self._feature_path = feature_path
        self._log_csv = open(self._log_csv_path, 'r')
        self._filtered_iter = self._mode_filter(self._log_csv, mode)

    def initialize(self):
        pass

    def extract(self):
        pass

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

    def _mode_filter(self, iter, mode):
        for cnt, line in enumerate(iter):
            if mode == 'debug' and cnt > self._DEBUG_LIMIT:
                break
            yield line

    def _parse_line(self, line):
        items = line.rstrip().split(',')
        dic = {
            'enrollment_id': items[0],
            'user_name': items[1],
            'course_id': items[2],
            'time': datetime.datetime.strptime(items[3], '%Y-%m-%dT%H:%M:%S'),
            'source': items[4],
            'event': items[5],
            'object': items[6]
        }
        return dic


