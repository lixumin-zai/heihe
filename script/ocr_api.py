# -*- coding: utf-8 -*-
from urllib import parse
import base64
import hashlib
import time
import requests
import json


'''
    1.图片属性：jpg/png/bmp,
    2.最短边至少15px，最长边最大4096px,
    3.编码后大小不超过4M,
    4.识别文字语种：中英文
    5.错误码链接：https://www.xfyun.cn/document/error-code
'''

# OCR手写文字识别接口地址
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
# 应用APPID(必须为webapi类型应用,并开通手写文字识别服务,参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
APPID = "8e0f0ea9"
# 接口密钥(webapi类型应用开通手写文字识别后，控制台--我的应用---手写文字识别---相应服务的apikey)
API_KEY = "ce7c692a7328ebe75cfbd974fcb9800d"


def getHeader(language, location):
    curTime = str(int(time.time()))
    param = "{\"language\":\""+language+"\",\"location\":\""+location+"\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()
    # 组装http请求头
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header

def getBody(imgfile):
    # with open(filepath, 'rb') as f:
    #     imgfile = f.read()
    data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
    return data

def call_api(imgfile):
    """"
    imgfile为 <class 'bytes'>
    """
    # 语种设置
    language = "cn|en"  # cn | en
    # 是否返回文本位置信息
    location = "false"  # true or false
    # 图片上传接口地址
    # picFilePath = "./23.png"
    headers = getHeader(language, location)
    r = requests.post(URL, headers=headers, data=getBody(imgfile))
    # print(r.text)
    text = json.loads(r.text)
    # print(text['data']['block']['line'])
    # print(type(text))

    text0 = ''
    for i in text["data"]["block"][0]['line'][1:]:
        # print(i['word'][0]["content"])
        text0 = text0 + i['word'][0]["content"]
    # print(text0)

    title = text["data"]["block"][0]['line'][0]['word'][0]["content"]
    section = []
    text1 = ''
    max_line = len(text["data"]["block"][0]['line'][1]['word'][0]["content"])
    # print(max_line)
    for i in text["data"]["block"][0]['line'][1:]:
        text1 = text1 + i['word'][0]["content"]
        # print(len(i['word'][0]["content"]))
        if len(i['word'][0]["content"]) < max_line:
            section.append(text1)
            text1 = ''
    return text0, title, section

if __name__ == "__main__":
    with open("../23.png", 'rb') as f:
        imgfile = f.read()
    text0, title, section = call_api(imgfile)
    # print(text0)
    # print("title:"+title)
    # print(section)
