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

# args
parser = argparse.ArgumentParser()
parser.add_argument('data_type', type=str, choices=['train', 'test'])
parser.add_argument('mode', type=str, nargs='?', default='debug', choices=['debug', 'normal'])


if __name__ == '__main__':
    data_type = parser.parse_args().data_type
    mode = parser.parse_args().mode
    extractor = EnrollmentFeatureExtractor(data_type, mode)
    extractor.extract()