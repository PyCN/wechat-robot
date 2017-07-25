#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Blueprint
from sanic.response import text
from wechatpy import parse_message
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
async def index(request):
    print('>>>', request.method)
    return text('hello, world')


@bp.route('/sign', methods=['GET', 'POST'])
async def signature(request):
    token = request.raw_args.get('token')
    signature = request.raw_args.get('signature')
    timestamp = request.raw_args.get('timestamp')
    nonce = request.raw_args.get('nonce')
    echostr = request.raw_args.get('echostr')
    print('>>>')
    if request.method == 'GET':
        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            # 处理异常情况或忽略
            print('>>>', request.raw_args, '验证异常')
            return text('验证异常')
        else:
            return text(echostr)
    elif request.method == 'POST':
        print('>>>', request.body)
        msg = parse_message(request.body)
        print('>>>>>', msg)
        return text(msg)
    return text('')
