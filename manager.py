#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import argparse
import os

from weapp import create_app

config_name = os.getenv('SANIC_CONFIG') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', default='0.0.0.0', help='ip')
    parser.add_argument('-p', '--port', default=8080, type=int, help='port number')
    parser.add_argument('-w', '--workers', default=2, type=int, help='number of process')
    args = parser.parse_args()
    print('>>>', args.ip)
    app.run(host=args.ip, port=args.port, workers=args.workers, debug=app.config.get('DEBUG'))
