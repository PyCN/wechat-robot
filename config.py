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
     欢迎使用wechat-robot,
     你可以试试如下命令：命令 内容
     
     快递 XXX
     天气 XXX
     翻译 XXX
     
     如：要翻译：我是谁？，请输入： 翻译 我是谁？
        要查询快递：12345678，请输入：快递 12345678
     
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
