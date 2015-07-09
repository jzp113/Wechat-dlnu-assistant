# -*- coding: utf-8 -*-
import requests
import json
def chatApi(text):
    UrlApi = 'http://www.tuling123.com/openapi/api?'
    payload = {'key':'55e7f30895a0a10535984bae5ad294d1',
               'info':text
               }
    r = requests.get(UrlApi, params=payload)
    text = json.loads(r.content)
    return text['text']

