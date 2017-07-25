#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Blueprint
from sanic.response import text
from wechatpy import parse_message
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply, ImageReply, VoiceReply
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
    if request.method == 'GET':
        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            # 处理异常情况或忽略
            print('>>>', request.raw_args, '验证异常')
            return text('验证异常')
        else:
            print('>>>', '验证ok')
            return text(echostr)
    elif request.method == 'POST':
        if len(request.body) == 0:
            return text('')
        request_msg = parse_message(request.body)
        request_msg_type = request_msg.type
        print('>>> {}\n{}\n{}'.format(request.body, request_msg_type, request_msg))
        reply = ''
        if request_msg_type == 'text':
            reply = TextReply(content='你所发的是文本:{}'.format(request_msg.content), message=request_msg)
        if request_msg_type == 'image':
            reply = ImageReply(message=request_msg)
            reply.media_id = request_msg.media_id
        if request_msg_type == 'voice':
            reply = VoiceReply(message=request_msg)
            reply.media_id = 'voice media id'

        # 返回xml报文
        xml = reply.render()
        return text(xml)

    return text('')
