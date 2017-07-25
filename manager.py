#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import os

from weapp import create_app

if __name__ == '__main__':
    app = create_app(os.getenv('SANIC_CONFIG') or 'default')
    app.run()
