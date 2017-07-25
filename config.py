#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    pass


class DevConfig(Config):
    DEBUG = True
    pass


class PrdConfig(Config):
    pass


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'default': DevConfig
}
