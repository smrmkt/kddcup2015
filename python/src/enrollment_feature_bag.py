#!/usr/bin/env python
#-*-coding:utf-8-*-

import ConfigParser
from collections import Counter
import datetime
import MySQLdb
import numpy as np
import os

from feature_bag import FeatureBag


base_dir = os.path.dirname(__file__)
event_types = ['problem', 'video', 'access', 'wiki', 'discussion', 'nagivate', 'page_close']

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

    def extract_access_days_per_week(self):
        access_dates = set([log['time'].strftime('%Y%m%d') for log in self.logs])
        access_dates = [datetime.datetime.strptime(d, '%Y%m%d') for d in access_dates]
        weeks = [0 for i in range(14)]
        start_date = datetime.datetime(2014, 5, 13)
        for access_date in access_dates:
            diff = (access_date-start_date).days/7
            weeks[diff] += 1
        for i, week in enumerate(weeks):
            self.feature_keys.append('access_days_week{0:02d}'.format(i))
            self.feature_values.append(week)
        return self

    def extract_access_interval_min(self):
        access_dates = sorted(list(set([log['time'].strftime('%Y%m%d') for log in self.logs])))
        access_dates = [datetime.datetime.strptime(d, '%Y%m%d') for d in access_dates]
        if len(access_dates) == 1:
            access_intervals = [0]
        else:
            access_intervals = [(access_dates[i+1]-access_dates[i]).days for i in range(len(access_dates)-1)]
        self.feature_keys.append('access_interval_min')
        self.feature_values.append(min(access_intervals))
        return self

    def extract_access_interval_max(self):
        access_dates = sorted(list(set([log['time'].strftime('%Y%m%d') for log in self.logs])))
        access_dates = [datetime.datetime.strptime(d, '%Y%m%d') for d in access_dates]
        if len(access_dates) == 1:
            access_intervals = [0]
        else:
            access_intervals = [(access_dates[i+1]-access_dates[i]).days for i in range(len(access_dates)-1)]
        self.feature_keys.append('access_interval_max')
        self.feature_values.append(max(access_intervals))
        return self

    def extract_access_interval_mean(self):
        access_dates = sorted(list(set([log['time'].strftime('%Y%m%d') for log in self.logs])))
        access_dates = [datetime.datetime.strptime(d, '%Y%m%d') for d in access_dates]
        if len(access_dates) == 1:
            access_intervals = [0]
        else:
            access_intervals = [(access_dates[i+1]-access_dates[i]).days for i in range(len(access_dates)-1)]
        self.feature_keys.append('access_interval_mean')
        self.feature_values.append(np.mean(access_intervals))
        return self

    def extract_access_interval_var(self):
        access_dates = sorted(list(set([log['time'].strftime('%Y%m%d') for log in self.logs])))
        access_dates = [datetime.datetime.strptime(d, '%Y%m%d') for d in access_dates]
        if len(access_dates) == 1:
            access_intervals = [0]
        else:
            access_intervals = [(access_dates[i+1]-access_dates[i]).days for i in range(len(access_dates)-1)]
        self.feature_keys.append('access_interval_var')
        self.feature_values.append(np.var(access_intervals))
        return self

    def extract_access_term(self):
        access_dates = set([log['time'] for log in self.logs])
        term = (max(access_dates)-min(access_dates)).days
        self.feature_keys.append('access_term')
        self.feature_values.append(term)
        return self

    def extract_access_hours(self):
        access_hours = sorted([log['time'].strftime('%H') for log in self.logs])
        counter = Counter(access_hours)
        for i in range(24):
            hour = '{0:02d}'.format(i)
            cnt = 0
            if hour in counter:
                cnt = counter[hour]
            self.feature_keys.append('access_hour_{0}'.format(hour))
            self.feature_values.append(cnt)
        return self

    def extract_access_hour_count(self):
        access_hours = set([log['time'].strftime('%H') for log in self.logs])
        self.feature_keys.append('access_hour_count')
        self.feature_values.append(len(access_hours))
        return self

    def extract_access_hour_mean(self):
        access_hours = [int(log['time'].strftime('%H')) for log in self.logs]
        self.feature_keys.append('access_hour_mean')
        self.feature_values.append(np.var(access_hours))
        return self

    def extract_access_hour_var(self):
        access_hours = [int(log['time'].strftime('%H')) for log in self.logs]
        self.feature_keys.append('access_hour_var')
        self.feature_values.append(np.var(access_hours))
        return self

    def extract_access_weekend_count(self):
        dows = [log['time'].weekday() for log in self.logs]
        self.feature_keys.append('access_weekend_count')
        self.feature_values.append(len([1 for d in dows if d > 5]))
        return self

    def extract_access_weekend_percentage(self):
        dows = [log['time'].weekday() for log in self.logs]
        self.feature_keys.append('access_weekend_percentage')
        self.feature_values.append(float(len([1 for d in dows if d > 5]))/len(dows))
        return self

    def extract_staytime_min(self):
        access_dates = [(log['time'].strftime('%Y%m%d'), log['time']) for log in self.logs]
        daily_logs = {}
        for d in access_dates:
            if d[0] in daily_logs.keys():
                daily_logs.get(d[0]).append(d[1])
            else:
                daily_logs[d[0]] = [d[1]]
        staytimes = [(max(v)-min(v)).seconds for k, v in daily_logs.items()]
        self.feature_keys.append('staytime_min')
        self.feature_values.append(min(staytimes))
        return self

    def extract_staytime_max(self):
        access_dates = [(log['time'].strftime('%Y%m%d'), log['time']) for log in self.logs]
        daily_logs = {}
        for d in access_dates:
            if d[0] in daily_logs.keys():
                daily_logs.get(d[0]).append(d[1])
            else:
                daily_logs[d[0]] = [d[1]]
        staytimes = [(max(v)-min(v)).seconds for k, v in daily_logs.items()]
        self.feature_keys.append('staytime_max')
        self.feature_values.append(max(staytimes))
        return self

    def extract_staytime_mean(self):
        access_dates = [(log['time'].strftime('%Y%m%d'), log['time']) for log in self.logs]
        daily_logs = {}
        for d in access_dates:
            if d[0] in daily_logs.keys():
                daily_logs.get(d[0]).append(d[1])
            else:
                daily_logs[d[0]] = [d[1]]
        staytimes = [(max(v)-min(v)).seconds for k, v in daily_logs.items()]
        self.feature_keys.append('staytime_mean')
        self.feature_values.append(np.mean(staytimes))
        return self

    def extract_staytime_var(self):
        access_dates = [(log['time'].strftime('%Y%m%d'), log['time']) for log in self.logs]
        daily_logs = {}
        for d in access_dates:
            if d[0] in daily_logs.keys():
                daily_logs.get(d[0]).append(d[1])
            else:
                daily_logs[d[0]] = [d[1]]
        staytimes = [(max(v)-min(v)).seconds for k, v in daily_logs.items()]
        self.feature_keys.append('staytime_var')
        self.feature_values.append(np.var(staytimes))
        return self

    def extract_source_count(self):
        sources = [log['source'] for log in self.logs]
        server_cnt = len([source for source in sources if source == 'server'])
        browser_cnt = len(sources) - server_cnt
        self.feature_keys.append('source_server_count')
        self.feature_values.append(server_cnt)
        return self

    def extract_event_count(self):
        events = sorted([log['event'] for log in self.logs])
        counter = Counter(events)
        for event_type in event_types:
            cnt = 0
            if event_type in counter:
                cnt = counter[event_type]
            self.feature_keys.append('event_{0}_count'.format(event_type))
            self.feature_values.append(cnt)
        return self

    def extract_event_percentage(self):
        events = sorted([log['event'] for log in self.logs])
        counter = Counter(events)
        for event_type in event_types:
            cnt = 0
            if event_type in counter:
                cnt = counter[event_type]
            self.feature_keys.append('event_{0}_percentage'.format(event_type))
            self.feature_values.append(float(cnt)/len(events))
        return self

    def extract_event_days_per_week(self):
        start_date = datetime.datetime(2014, 5, 13)
        event_week = {}
        for event_type in event_types:
            event_week[event_type] = [0 for i in range(82/7+1)]
        targets = set(['{0},{1}'.format(log['time'].strftime('%Y%m%d'), log['event']) for log in self.logs])
        for target in targets:
            d, e = target.split(',')
            diff = (datetime.datetime.strptime(d, '%Y%m%d')-start_date).days/7
            event_week[e][diff] += 1
        for event, weeks in event_week.items():
            for i, week in enumerate(weeks):
                self.feature_keys.append('event_days_{0}_week{1:02d}'.format(event, i))
                self.feature_values.append(week)
        return self

    def extract_video_over10minutes_count_per_week(self):
        start_date = datetime.datetime(2014, 5, 13)
        weeks = [0 for i in range(14)]
        for i in range(len(self.logs)-1):
            if self.logs[i]['event'] != 'video':
                continue
            time_delta = self.logs[i+1]['time']-self.logs[i]['time']
            if 600 < time_delta.seconds < 18000 and time_delta.days == 0:
                diff = (self.logs[i+1]['time']-start_date).days/7
                weeks[diff] += 1
        for i, week in enumerate(weeks):
            self.feature_keys.append('video_over10minutes_week{0:02d}'.format(i))
            self.feature_values.append(week)
        return self

    def extract_problem_over3minutes_count_per_week(self):
        start_date = datetime.datetime(2014, 5, 13)
        weeks = [0 for i in range(14)]
        for i in range(len(self.logs)-1):
            if self.logs[i]['event'] != 'video':
                continue
            time_delta = self.logs[i+1]['time']-self.logs[i]['time']
            if 180 < time_delta.seconds < 18000 and time_delta.days == 0:
                diff = (self.logs[i+1]['time']-start_date).days/7
                weeks[diff] += 1
        for i, week in enumerate(weeks):
            self.feature_keys.append('problem_over3minutes_week{0:02d}'.format(i))
            self.feature_values.append(week)
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
