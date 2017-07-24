#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Sanic
from sanic.response import json, text

main = Sanic(__name__)


@main.route('/interface')
async def interface(request):
    return json({"received": True, "message": request.json})


@main.route('/sign', methods=['GET'])
def signature(request):
    print('>>>', request.raw_args)
    return text(request.raw_args.get('echostr'))


if __name__ == '__main__':
    main.run(host='0.0.0.0', port=8080, debug=True)
