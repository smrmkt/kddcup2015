#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
import os.path
import sys

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src')

from access_feature_extractor import AccessFeatureExtractor

# args
parser = argparse.ArgumentParser()
parser.add_argument('data_type', type=str, choices=['train', 'test'])


if __name__ == '__main__':
    data_type = parser.parse_args().data_type
    extractor = AccessFeatureExtractor(data_type)
    extractor.extract()