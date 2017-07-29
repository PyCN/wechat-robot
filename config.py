#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    WECHAT_TOKEN = os.environ.get('WECHAT_TOKEN') or 'hard to guess string'
    WECHAT_ENCODING_AES_KEY = os.environ.get('WECHAT_ENCODING_AES_KEY') or 'hard to guess string'
    WECHAT_APPID = os.environ.get('WECHAT_APPID') or 'hard to guess string'

    WELCOME_MSG = '''
     能聊天，能识别图片人物年龄，
     能解析语音，能讲笑话
     上知天文下知地理，学富五车才高八斗
     --------------------------
     来来来，帮你排忧解难。。。
    '''

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
