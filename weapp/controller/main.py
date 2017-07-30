#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
import json
import os

import requests
from gtts import gTTS
from sanic import Blueprint, response
from sanic.log import log, netlog
from translate import Translator
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import TextReply, EmptyReply
from wechatpy.utils import check_signature

import config
from weapp.controller.howold import howold
from weapp.controller.kuaidi import KuaiDi

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
async def index(request):
    return response.redirect('http://www.sina.com.cn')


@bp.route('/interface', methods=['GET', 'POST'])
async def interface(request):
    # get var from request args
    signature = request.raw_args.get('signature', '')
    timestamp = request.raw_args.get('timestamp', '')
    nonce = request.raw_args.get('nonce', '')
    echostr = request.raw_args.get('echostr', '')
    msg_signature = request.raw_args.get('msg_signature', '')
    encrypt_type = request.raw_args.get('encrypt_type', '')

    try:
        check_signature(config.WECHAT_TOKEN, signature, timestamp, nonce)
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
                crypto = WeChatCrypto(config.WECHAT_TOKEN, config.WECHAT_ENCODING_AES_KEY, config.WECHAT_APPID)
                try:
                    decrypted_xml = crypto.decrypt_message(
                        request.body,
                        msg_signature,
                        timestamp,
                        nonce
                    )
                except (InvalidAppIdException, InvalidSignatureException):
                    # to-do: 处理异常或忽略
                    log.error('>>> 加密处理异常')
                    return response.text('')
                else:
                    return response.text(get_resp_message(request, decrypted_xml, mode='aes'))
            else:
                # 纯文本方式
                return response.text(get_resp_message(request, request.body))


def get_resp_message(request, source_msg, mode=None):
    request_msg = parse_message(source_msg)
    request_msg_type = request_msg.type
    log.info('>>> body[{}],request_msg_type[{}],request_msg[{}]'.format(request.body, request_msg_type, request_msg))
    # 根据消息类型解析
    if request_msg_type == 'text':
        reply = TextReply(content='{}'.format(get_text_reply(request, request_msg.content)), message=request_msg)
    elif request_msg_type == 'image':
        # reply = ImageReply(message=request_msg)
        # reply.media_id = request_msg.media_id
        reply = TextReply(content=howold(request_msg.image), message=request_msg)
    elif request_msg_type == 'voice':
        if not request_msg.recognition:
            reply = TextReply(content='没听清楚啊，再说一遍，亲', message=request_msg)
        else:
            content = get_text_reply(request, request_msg.recognition)
            tts = gTTS(text=content, lang='zh-cn')
            tts.save(os.path.join(config.SPEECH_DATA_DIR, 'good.mp3'))

            reply = TextReply(content='{}'.format(content), message=request_msg)
    elif request_msg_type == 'event':
        request_msg_event = request_msg.event
        if request_msg_event == 'subscribe':
            reply = TextReply(content=request.app.config.get('WELCOME_MSG'), message=request_msg)
        elif request_msg_event == 'unsubscribe':
            reply = TextReply(content='多谢关注！', message=request_msg)
        else:
            reply = EmptyReply()
    else:
        reply = EmptyReply()

    # 返回xml报文
    xml = reply.render()

    if mode == 'aes':
        # get var
        timestamp = request.raw_args.get('timestamp', '')
        nonce = request.raw_args.get('nonce', '')

        crypto = WeChatCrypto(config.WECHAT_TOKEN, config.WECHAT_ENCODING_AES_KEY, config.WECHAT_APPID)
        encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
        return encrypted_xml
    else:
        return xml


def get_text_reply(request, text):
    openid = request.raw_args.get('openid', '')
    do_type = text[:2]
    if do_type == '翻译' or do_type == 'fy':
        resp = text_translate(text[2:])
    elif do_type == '快递' or do_type == 'kd':
        resp = text_kuaidi(text[2:])
        if not resp:
            # resp = 'ooo, 你输入的快递没有查到，请到官网查询试试!'
            resp = text_tuling(text, openid)
    else:
        resp = text_tuling(text, openid)
    return resp


def text_translate(text):
    if not text:
        return None
    translator = Translator(from_lang='zh', to_lang="en")
    return translator.translate(text)


def text_kuaidi(text):
    kd = KuaiDi()
    return kd.get_kuaidi(text)


def text_tuling(text, userid=None):
    if len(text) == 0:
        return '请输入正确的文本'
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {"key": config.TULING_APIKEY, "info": text, "userid": userid}

    r = requests.post(api_url, data=data)
    if r.status_code == 200:
        rsp = json.loads(r.text)
        tuling_text = rsp.get('text')
        tuling_url = rsp.get('url', '')
        print('>>>', r.text)
        if tuling_url:
            return ':'.join([tuling_text, tuling_url])
        else:
            return tuling_text

    return '请输入正确的文本'


if __name__ == '__main__':
    # print(text_tuling('今日新闻'))
    pass
