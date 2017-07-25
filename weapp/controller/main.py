#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Blueprint
from sanic.response import json, text

bp = Blueprint('main', __name__)


@bp.route('/')
def index(request):
    return text('hello, world')


@bp.route('/interface')
async def interface(request):
    return json({"received": True, "message": request.json})


@bp.route('/sign', methods=['GET'])
def signature(request):
    print('>>>', request.raw_args)
    return text(request.raw_args.get('echostr'))
