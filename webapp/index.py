#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Sanic
from sanic.response import json

main = Sanic(__name__)


@main.route('/interface')
async def interface(request):
    return json({"received": True, "message": request.json})


@main.route('/sign', methods=['GET'])
def signature(request):
    print('>>>', request.raw_args)
    return json(request.raw_args)


if __name__ == '__main__':
    main.run(host='0.0.0.0', port=80, debug=True)
