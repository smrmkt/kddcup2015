#!/usr/bin/env python
#-*-coding:utf-8-*-

from collections import Counter

from feature_bag import FeatureBag


class EnrollmentFeatureBag(FeatureBag):
    def __init__(self, enrollment_id, logs, feature_keys, feature_values):
        FeatureBag.__init__(self, enrollment_id, logs, feature_keys, feature_values)

    def extract_access_count(self):
        self.feature_keys.append('access_count')
        self.feature_values.append(len(self.logs))
        return self

    def extract_access_days(self):
        access_dates = set([log['time'].strftime('%Y%m%d') for log in self.logs])
        self.feature_keys.append('access_days')
        self.feature_values.append(len(access_dates))
        return self

    def extract_access_hours(self):
        access_hours = [log['time'].strftime('%H') for log in self.logs]
        counter = Counter(access_hours)
        for i in range(24):
            hour = '{0:02d}'.format(i)
            cnt = 0
            if hour in counter:
                cnt = counter[hour]
            self.feature_keys.append('access_hour_{0}'.format(hour))
            self.feature_values.append(cnt)
        return self

    def extract_source_count(self):
        sources = [log['source'] for log in self.logs]
        server_cnt = len([source for source in sources if source == "server"])
        browser_cnt = len(sources) - server_cnt
        self.feature_keys.append('source_server_count')
        self.feature_values.append(server_cnt)
        self.feature_keys.append('source_browser_count')
        self.feature_values.append(browser_cnt)
        return self

    def extract_event_count(self):
        events = [log['event'] for log in self.logs]
        counter = Counter(events)
        for event in ['problem', 'video', 'access', 'wiki', 'discussion', 'navigate', 'page_close']:
            cnt = 0
            if event in counter:
                cnt = counter[event]
            self.feature_keys.append('event_{0}'.format(event))
            self.feature_values.append(cnt)
        return self
