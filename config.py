#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    pass


class DevConfig(Config):
    SANIC_DEBUG = True

    def __init__(self):
        print('>>> current config: dev')

    pass


class PrdConfig(Config):
    SANIC_DEBUG = False

    def __init__(self):
        print('>>> current config: prd')

    pass


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'default': DevConfig
}
