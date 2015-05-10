#!/usr/bin/env python
#-*-coding:utf-8-*-

from collections import Counter

from feature_bag import FeatureBag


class UserFeatureBag():
    def __init__(self, user_name, logs):
        self.user_name = user_name
        self.logs_group = self._group_logs(logs)
        self.feature_keys = []
        self.feature_values_group = {k: [] for k, v in self.logs_group.items()}

    def _group_logs(self, logs):
        dic = {}
        for log in logs:
            enrollment_id = log['enrollment_id']
            if enrollment_id in dic:
                dic[enrollment_id].append(log)
            else:
                dic[enrollment_id] = [log]
        return dic

    def extract_course_count(self):
        self.feature_keys.append('course_count')
        for k, v in self.feature_values_group.items():
            v.append(len(self.logs_group))
        return self

    def extract_course_access_percentage(self):
        self.feature_keys.append('course_access_percentage')
        access_count = sum([len(v) for k, v in self.logs_group.items()])
        for k, v in self.logs_group.items():
            self.feature_values_group[k].append(float(len(v))/access_count)
        return self