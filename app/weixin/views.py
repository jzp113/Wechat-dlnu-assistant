# -*- coding: utf-8 -*-

from flask import render_template
from flask import Blueprint
from flask import request
from flask import make_response

from checkevent import checkevent
from chat_api import chatApi

import urllib
import urllib2
from urllib import urlencode
import json
import time
import hashlib
import xml.etree.ElementTree as ET

weixin = Blueprint('weixin', __name__, template_folder = 'templates')

@weixin.route('/weixin',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='jzp113'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        event = xml_rec.find('Event')
        event_key = xml_rec.find('EventKey')
        content = xml_rec.find('Content')

        if content is not None:
            contents = chatApi(content.text)
        elif event.text == 'subscribe':
            key = 'subscribe'
            contents = checkevent(fromu).key_check(key)
        else:
            key = event_key.text
            contents = checkevent(fromu).key_check(key)


        return render_template('reply_text.xml',
        toUser = fromu,
        fromUser = tou,
        createtime = str(int(time.time())),
        content = contents
        )

