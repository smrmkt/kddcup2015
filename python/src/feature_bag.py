#!/usr/bin/env python
#-*-coding:utf-8-*-

class FeatureBag():
    def __init__(self, group_id, logs, feature_keys, feature_values):
        self.group_id = group_id
        self.feature_keys = feature_keys
        self.feature_values = feature_values
        self.logs = logs
