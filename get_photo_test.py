# python3.7
# -*- coding: utf-8 -*-
# @Author : listen
# @Time   :
import requests
import base64
import json
from requests_toolbelt import MultipartEncoder


# API地址
url = "http://192.168.10.113:8888/photo"
# 图片地址
# file_path = 'C:/Users/Administrator/Desktop/23.png'
file_path = 'C:/Users/Administrator/Desktop/1.jpg'
# 图片名
file_name = file_path.split('/')[-1]
# 二进制打开图片
file = open(file_path, 'rb')
# a = file.read()
# print(type(a))
# 拼接参数
data0 = MultipartEncoder(
    fields={"username": "黎旭民", 'page': "1", "file": (file_name, file)}
    )
# files = {'file': (file_name, file)}

# 发送post请求到服务器端
r = requests.post(url, data=data0, verify=False, headers={'Content-Type': data0.content_type})
# print(r.headers)
# 获取服务器返回的图片，字节流返回
result = r.text
# 字节转换成图片
print(result)
# img = base64.b64decode(result)
# file = open('test.jpg', 'wb')
# file.write(img)
# file.close()