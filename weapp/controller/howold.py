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

    result = []
    for i in json.loads(AnalyticsEvent):
        face = i.get('face')
        age = face.get('age', '不知道多大')

        # update
        if face.get('gender') == 'Female':
            if age < 10:
                gender = '且漂亮可爱的小姑娘'
            else:
                gender = '且漂亮可爱的靓妹'
        else:
            gender = '且英气逼人的帅哥'
        result.append('一位年龄大约{}岁，{}'.format(age, gender))

    if len(result) == 0:
        return random.choice(['算你狠，居然没有识别出来', '算了吧，不确定，是不是无性别人士'])
    else:
        return '我看到{}位，{}'.format(len(result), ','.join(result))


if __name__ == '__main__':
    pic = ''

    print(howold(pic))
