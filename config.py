#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    WECHAT_TOKEN = os.environ.get('WECHAT_TOKEN') or 'hard to guess string'

    @classmethod
    def init_app(cls, app):
        pass


class DevConfig(Config):
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # log to stderr


class PrdConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

    pass


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'default': PrdConfig
}
