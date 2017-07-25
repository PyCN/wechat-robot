#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Blueprint
from sanic.response import json, text

from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

bp = Blueprint('main', __name__)


@bp.route('/')
async def index(request):
    return text('hello, world')


@bp.route('/interface')
async def interface(request):
    return json({"received": True, "message": request.json})


@bp.route('/sign', methods=['GET'])
async def signature(request):
    token = request.raw_args.get('token')
    signature = request.raw_args.get('signature')
    timestamp = request.raw_args.get('timestamp')
    nonce = request.raw_args.get('nonce')
    echostr = request.raw_args.get('echostr')

    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        # 处理异常情况或忽略
        print('>>>', request.raw_args, '验证异常')
        return text('验证异常')
    else:
        return text(echostr)
