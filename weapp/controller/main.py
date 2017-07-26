#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from sanic import Blueprint, response
from sanic.log import log, netlog
from translate import Translator
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import TextReply, ImageReply, VoiceReply, EmptyReply
from wechatpy.utils import check_signature

from .kuaidi import KuaiDi

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
async def index(request):
    return response.redirect('http://www.sina.com.cn')


@bp.route('/interface', methods=['GET', 'POST'])
async def interface(request):
    # get var from config file
    token = request.app.config.get('WECHAT_TOKEN', None)
    encoding_aes_key = request.app.config.get('WECHAT_ENCODING_AES_KEY', None)
    appid = request.app.config.get('WECHAT_APPID', None)

    # get var from request args
    signature = request.raw_args.get('signature', '')
    timestamp = request.raw_args.get('timestamp', '')
    nonce = request.raw_args.get('nonce', '')
    echostr = request.raw_args.get('echostr', '')
    msg_signature = request.raw_args.get('msg_signature', '')
    encrypt_type = request.raw_args.get('encrypt_type', '')

    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        # 处理异常情况或忽略
        netlog.error('>>> {},{}'.format(request.raw_args, '验证异常'))
        return response.text('验证异常')
    else:
        if request.method == 'GET':
            # 服务器配置
            log.info('>>> {},{}'.format(request.raw_args, '验证ok'))
            return response.text(echostr)
        else:
            # 公众号被动接受消息
            if len(request.body) == 0:
                return response.text('')

            # 加密方式
            if encrypt_type == 'aes':
                crypto = WeChatCrypto(token, encoding_aes_key, appid)
                try:
                    decrypted_xml = crypto.decrypt_message(
                        request.body,
                        msg_signature,
                        timestamp,
                        nonce
                    )
                except (InvalidAppIdException, InvalidSignatureException):
                    # to-do: 处理异常或忽略
                    return response.text('')
                else:
                    request_msg = parse_message(decrypted_xml)
            else:
                # 纯文本方式
                request_msg = parse_message(request.body)

            request_msg_type = request_msg.type
            log.info('>>> request.body[{}],request_msg_type[{}],request_msg[{}]'.format(request.body, request_msg_type,
                                                                                        request_msg))
            # 根据消息类型解析
            if request_msg_type == 'text':
                reply = text_reply(request_msg.content, request_msg)
            elif request_msg_type == 'image':
                reply = ImageReply(message=request_msg)
                reply.media_id = request_msg.media_id
            elif request_msg_type == 'voice':
                reply = VoiceReply(message=request_msg)
                reply.media_id = request_msg.media_id
            elif request_msg_type == 'event':
                print('>>>'*30)
                reply = TextReply(content='多谢关注！', message=request_msg)
            else:
                reply = EmptyReply()

            # 返回xml报文
            xml = reply.render()
            return response.text(xml)


def text_reply(text, req_msg):
    do_type = text[:2]
    if do_type == '翻译' or do_type == 'fy':
        resp = text_translate(text[2:])
    elif do_type == '快递' or do_type == 'kd':
        resp = text_kuaidi(text[2:])
    else:
        resp = 'ooo, 不明白你的意思!'
    return TextReply(content='{}'.format(resp), message=req_msg)


def text_translate(text):
    if not text:
        return None
    translator = Translator(from_lang='zh', to_lang="en")
    return translator.translate(text)


def text_kuaidi(text):
    kd = KuaiDi()
    return kd.get_kuaidi(text)
