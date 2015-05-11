#!/usr/bin/env python
#-*-coding:utf-8-*-

import ConfigParser
from collections import Counter
import MySQLdb
import os

from feature_bag import FeatureBag


base_dir = os.path.dirname(__file__)

class EnrollmentFeatureBag(FeatureBag):
    def __init__(self, enrollment_id, logs, feature_keys, feature_values):
        conf = ConfigParser.SafeConfigParser()
        conf.read('{0}/../settings.conf'.format(base_dir))
        self._con = MySQLdb.connect(
            host=conf.get('mysql', 'host'),
            db=conf.get('mysql', 'db'),
            user=conf.get('mysql', 'user'),
            passwd=conf.get('mysql', 'passwd'),
        )
        FeatureBag.__init__(self, enrollment_id, logs, feature_keys, feature_values)

    def __del__(self):
        self._con.close()

    def extract_access_count(self):
        self.feature_keys.append('access_count')
        self.feature_values.append(len(self.logs))
        return self

    def extract_access_days(self):
        access_dates = set([log['time'].strftime('%Y%m%d') for log in self.logs])
        self.feature_keys.append('access_days')
        self.feature_values.append(len(access_dates))
        return self

    def extract_access_term(self):
        access_dates = set([log['time'] for log in self.logs])
        term = (max(access_dates)-min(access_dates)).days
        self.feature_keys.append('access_term')
        self.feature_values.append(term)
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
        server_cnt = len([source for source in sources if source == 'server'])
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

    def extract_courses(self):
        course_id = self.logs[0]['course_id']
        cursor = self._con.cursor()
        cursor.execute('SELECT rank FROM course WHERE course_id="{0}"'.format(course_id))
        rank = cursor.fetchone()[0]
        cursor.close()
        for i in range(1, 40):
            self.feature_keys.append('course_rank_{0:02d}'.format(i))
            if rank == i:
                self.feature_values.append(1)
            else:
                self.feature_values.append(0)
        return self

    def extract_course_audience(self):
        course_id = self.logs[0]['course_id']
        cursor = self._con.cursor()
        cursor.execute('SELECT audience FROM course WHERE course_id="{0}"'.format(course_id))
        self.feature_keys.append('course_audience')
        self.feature_values.append(cursor.fetchone()[0])
        cursor.close()
        return self
