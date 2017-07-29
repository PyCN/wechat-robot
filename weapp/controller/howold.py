#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

import json
import random

import requests


def howold(picurl):
    s = requests.session()
    url = 'https://how-old.net/Home/Analyze?isTest=False&source=&version=how-old.net'
    header = {
        'Host': 'how-old.net',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': 'https://how-old.net',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'x-ms-request-root-id': '8LGSI',
        'Content-Type': 'application/octet-stream',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'x-ms-request-id': 'eaNSR',
        'DNT': '1',
        'Referer': 'https://how-old.net/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    r = s.post(url, data=s.get(picurl).content, headers=header)
    resp = json.loads(r.text)
    resp = json.loads(resp)
    AnalyticsEvent = resp.get('AnalyticsEvent')
    face = json.loads(AnalyticsEvent)[0].get('face')
    if not face:
        return random.choice(['算你狠，居然没有识别出来', '算了吧，不确定，是不是无性别人士'])
    else:
        age = face.get('age', '不知道多大')
        if face.get('gender') == 'Female':
            if age < 5:
                gender = '且漂亮可爱的小姑娘'
            else:
                gender = '且漂亮可爱的靓妹'
        else:
            gender = '且英气逼人的帅哥'

        return '我看到一位年龄大约{}岁，{}'.format(age, gender)


if __name__ == '__main__':
    # picurl = 'http://mmbiz.qpic.cn/mmbiz_jpg/YnxvCtAax45Cia7rziaCAVW7j32V3iaDaGYBULUqtHGAic4CJE3RQUkAibstOKC1tyeibicfKuxlrfjQehEqg0IN2qg3g/0'
    # picurl = 'http://mmbiz.qpic.cn/mmbiz_jpg/YnxvCtAax45Cia7rziaCAVW7j32V3iaDaGYzelPkSeK9iaXEahiaxdWLuRPtc7fiabdynEJjd3X9sB4DraY8tkEzR0fg/0'
    picurl = 'http://mmbiz.qpic.cn/mmbiz_jpg/YnxvCtAax45Cia7rziaCAVW7j32V3iaDaGY4whLPz6Fe9IA00OW5awHG1Zhz1iczcWM3Lr3Mbd0ZGVACMXLBbdq7wQ/0'
    res = howold(picurl)
    print(res)
