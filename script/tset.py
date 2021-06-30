# python3.7
# -*- coding: utf-8 -*-
# @Author : listen
# @Time   :

import json

text = '''
{
  "code": "0",
  "data": {
    "block": [
      {
        "type": "text",
        "line": [
          {
            "confidence": 1,
            "word": [
              {
                "content": "要求：题目自拟，立意目定，"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "致敬打工人"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "“打工人，打工魂，打工人是人上人！”相信各"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "位对这句话应该不陌生自从“打工人”这一词在"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "网络上火起来后，便在生活中随处可见。那么，大"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "家是否了解所谓的“打工人“呢？"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "体力劳动都者或技术劳动者，是我们对打工人"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "的普遍认知，无论是在工地搬砖的工人还是坐在办"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "公室中的白领，在工作一天之后总会身心玻惫而"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "一句“世上只有两种最耀眼的光芒，一种是太阳"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "一种是打工人努力的模样”便给予了他们极大的"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "鼓励，也赋予了他们积极面对生活的心态。以前的"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "办公室白领总被人们称为“社畜”，这未免是有些"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "消极意味的，而打工人”这一新名词的发掘"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "使人们眼前焕然一新。他是们不止是为公司打工"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "更是为自己打工。"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "“累吗？累就对了。早中，打工人！”这样简单"
              }
            ]
          },
          {
            "confidence": 1,
            "word": [
              {
                "content": "的一句话，体现了打工人对生活的热爱和积极，"
              }
            ]
          }
        ]
      }
    ]
  },
  "desc": "success",
  "sid": "wcr00056cf7@gzadc71436115c460e00"
}'''

a = json.loads(text)

print(type(a["data"]))
# print(a["data"]["block"][0]['line'])
text0=''
for i in a["data"]["block"][0]['line']:
    print(i['word'][0]["content"])
    text0 = text0 + i['word'][0]["content"]

print(text0)