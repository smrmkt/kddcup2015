#!/usr/bin/env python
#-*-coding:utf-8-*-

import itertools
import os.path

from enrollment_feature_bag import EnrollmentFeatureBag
from feature_extractor import FeatureExtractor

base_dir = os.path.dirname(__file__)


class EnrollmentFeatureExtractor(FeatureExtractor):
    def __init__(self, data_type, mode, debug_limit):
        log_csv_path = '{0}/../data/{1}/log_{1}.csv'.format(base_dir, data_type)
        feature_path = '{0}/../data/feature/enrollment_feature_{1}.csv'.format(base_dir, data_type)
        FeatureExtractor.__init__(self, mode, log_csv_path, feature_path, debug_limit)

    def extract(self):
        tuple_iter = self._tuple_generator(self._filtered_iter)
        grouped_iter = itertools.groupby(tuple_iter, lambda x: x[0])
        bag_iter = self._bag_generator(grouped_iter)
        feature_iter = self._extract_enrollment_features(bag_iter)
        self._save_to_file(feature_iter)
        self._log_csv.close()

    def _extract_enrollment_features(self, iter):
        for bag in iter:
            yield bag.extract_access_count()\
                .extract_access_days()\
                .extract_access_interval_min()\
                .extract_access_interval_max()\
                .extract_access_interval_mean()\
                .extract_access_interval_var()\
                .extract_access_days_per_week()\
                .extract_access_term()\
                .extract_access_hour_count()\
                .extract_access_hour_mean()\
                .extract_access_hour_var()\
                .extract_access_weekend_count()\
                .extract_access_weekend_percentage()\
                .extract_staytime_min()\
                .extract_staytime_max()\
                .extract_staytime_mean()\
                .extract_staytime_var()\
                .extract_source_count()\
                .extract_event_count()\
                .extract_event_days_per_week()\
                .extract_event_percentage()\
                .extract_video_over10minutes_count_per_week()\
                .extract_courses()\
                .extract_course_audience()

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
                    str(bag.group_id),
                    ','.join([str(v)for v in bag.feature_values])
                ))

    def _tuple_generator(self, iter):
        for line in iter:
            enrollment_id = (line.split(','))[0]
            if str.isdigit(enrollment_id):
                yield (int(enrollment_id), self._parse_line(line))

    def _bag_generator(self, iter):
        for k, g in iter:
            yield EnrollmentFeatureBag(k, [t[1] for t in g], [], [])
