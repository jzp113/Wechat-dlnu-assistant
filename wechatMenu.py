# -*- encoding: utf-8 -*-

import urllib
import urllib2
from urllib import urlencode
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

appid = ''
secret = ''

gettoken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret

f = urllib2.urlopen( gettoken )


stringjson = f.read()

access_token = json.loads(stringjson)['access_token']

print access_token

posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token
getMenu = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=" + access_token

menu = '''{
    "button": [
        {
            "name": "账户", 
            "sub_button": [
                {
                    "type": "click", 
                    "name": "绑定账户", 
                    "key": "binding"
                }, 
                {
                    "type": "click", 
                    "name": "解除绑定", 
                    "key": "unlock"
                }, 
                {
                    "type": "click", 
                    "name": "课程更新", 
                    "key": "updatecourses"
                }, 
                {
                    "type": "click", 
                    "name": "校园网下线", 
                    "key": "drcom_logout"
                }
            ]
        }, 
        {
            "name": "校园大杂烩", 
            "sub_button": [
                {
                    "type": "click", 
                    "name": "近期成绩", 
                    "key": "grade"
                }, 
                {
                    "type": "click", 
                    "name": "课表助手", 
                    "key": "course"
                }, 
                {
                    "type": "click", 
                    "name": "借阅信息", 
                    "key": "book_list"
                }, 
                {
                    "type": "click", 
                    "name": "图书续期", 
                    "key": "delaybook"
                }, 
                {
                    "type": "click", 
                    "name": "流量监控", 
                    "key": "drcom_flow"
                }
            ]
        }, 
        {
            "name": "大杂烩②", 
            "sub_button": [
                {
                    "type": "click", 
                    "name": "使用手册", 
                    "key": "userguide"
                }, 
                {
                    "type": "click", 
                    "name": "补考成绩", 
                    "key": "resitgrade"
                }, 
                {
                    "type": "click", 
                    "name": "鄙人自序", 
                    "key": "codeinfo"
                }, 
                {
                    "type": "click", 
                    "name": "彩蛋", 
                    "key": "eggs"
                }, 
                {
                    "type": "click", 
                    "name": "最近考试", 
                    "key": "testinfo"
                }
            ]
        }
    ]
}'''

#request = urllib2.urlopen(getMenu)
request = urllib2.urlopen(posturl, menu.encode('utf-8'))

print request.read()


