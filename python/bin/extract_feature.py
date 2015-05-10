#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
import os.path
import sys

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src')

from enrollment_feature_extractor import EnrollmentFeatureExtractor
from user_feature_extractor import UserFeatureExtractor

# args
parser = argparse.ArgumentParser()
parser.add_argument('target', type=str, choices=['enrollment', 'user'], default='enrollment')
parser.add_argument('data_type', type=str, choices=['train', 'test'], default='train')
parser.add_argument('mode', type=str, choices=['debug', 'normal'], nargs='?', default='debug')


if __name__ == '__main__':
    target = parser.parse_args().target
    data_type = parser.parse_args().data_type
    mode = parser.parse_args().mode
    extractor = None
    if target == 'enrollment':
        extractor = EnrollmentFeatureExtractor(data_type, mode)
    elif target == 'user':
        extractor = UserFeatureExtractor(data_type, mode)
    extractor.extract()