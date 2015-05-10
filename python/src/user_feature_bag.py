#!/usr/bin/env python
#-*-coding:utf-8-*-

from collections import Counter

from feature_bag import FeatureBag


class UserFeatureBag(FeatureBag):
    def __init__(self, user_name, logs, feature_keys, feature_values):
        FeatureBag.__init__(self, user_name, logs, feature_keys, feature_values)

    def extract_course_count(self):
        courses = set([log['course_id'] for log in self.logs])
        self.feature_keys.append('course_count')
        self.feature_values.append(len(courses))
        return self
