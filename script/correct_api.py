#
# 文本纠错 WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret、要纠错文本信息text
# 运行方法：直接运行 main 即可
# 结果： 控制台输出结果信息
#
# 接口文档（必看）：https://www.xfyun.cn/doc/nlp/textCorrection/API.html
#
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import os
import traceback
import json
import requests


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


# calculate sha256 and encode to base64
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="POST", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    # print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)


def call_api(text):
    # 控制台获取
    APPId = "f2abae25"
    # 控制台获取
    APISecret = "MmM2YWY4MGY5YWY0MmJjMzhlYzU5ZGE4"
    # 控制台获取
    APIKey = "fd45f48d4a8def7e72bba80a065f78a8"
    # 需纠错文本

    Text = text

    url = 'https://api.xf-yun.com/v1/private/s9a87e3ec'

    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "s9a87e3ec": {
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "input": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 3,
                "text": base64.b64encode(Text.encode("utf-8")).decode('utf-8')
            }
        }
    }

    request_url = assemble_ws_auth_url(url, "POST", APIKey, APISecret)

    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': APPId}
    # print(request_url)
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    # print(response)
    # print('response==>>\n' + response.content.decode())
    tempResult = json.loads(response.content.decode())
    # print(type(tempResult))
    result = base64.b64decode(tempResult['payload']['result']['text']).decode()
    # print(base64.b64decode(tempResult['payload']['result']['text']).decode())
    correct_text = json.loads(result)
    # print(correct_text)
    err = []
    for err_type in correct_text:   # 获取全部错误
        for err0 in correct_text[err_type]:
            err.append(err0)
    err = sorted(err, key=lambda i: i[0], reverse=True)  # 以错误位置倒叙排序错误
    posde = 0
    for temp in err:
        if posde != int(temp[0]):
            Text1 = Text[:int(temp[0])]
            Text2 = Text[int(temp[0]) + len(temp[1]):]
            Text = Text1 + temp[2] + Text2
            posde = int(temp[0])
    return Text


if __name__ == '__main__':
    Text = "莫过共握手！――题记虚掩的房门“咯吱”一声开了一道缝隙，" \
           "爸探进半个脑袋向里张望。天刚亮，同房的病友可能正在梦乡。"
    # correct = call_api(Text)
    # print(type(correct))
    # correct_text = json.loads(correct)
    correct_text = {
        "char": [
            [
                28,
                "爸",
                "我",
                "char"
            ]
        ],
        "word": [],
        "redund": [
            [
                1,
                "过共",
                "",
                "red"
            ]
        ],
        "miss": [],
        "order": [],
        "dapei": [],
        "punc": [],
        "idm": [],
        "org": [],
        "leader": [],
        "number": []
    }
    # correct_text.pop('word', )
    err = []
    for err_type in correct_text:
        for err0 in correct_text[err_type]:
            err.append(err0)
    err = sorted(err, key=lambda i: i[0], reverse=True)
    for temp in err:
        Text = Text[:int(temp[0])] + temp[2] + Text[int(temp[0]) + len(temp[1]):]

    print(err)
    print(Text)
