#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import argparse
import os

from weapp import create_app

app = create_app(os.getenv('SANIC_CONFIG') or 'default')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--host', default='0.0.0.0', help='ip')
    parser.add_argument('-p', '--port', default=8080, type=int, help='port number')
    parser.add_argument('-w', '--workers', default=2, type=int, help='number of process')
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, workers=args.workers)
