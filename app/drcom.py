#encoding:utf-8
import requests
import HTMLParser
import urlparse
import string
import re
import hashlib
import time
from bs4 import BeautifulSoup

class drcom:
    def __init__(self, username, password):

        self.username = username
        self.password = hashlib.md5(password).hexdigest()


        self.login_url = 'http://210.30.1.112:8089/Self/LoginAction.action'
        self.random_url = 'http://210.30.1.112:8089/Self/RandomCodeAction.action'
        self.logout_sessionid_url = 'http://210.30.1.112:8089/Self/nav_offLine' #get the session id
        self.logout_url = 'http://210.30.1.112:8089/Self/tooffline'
        self.getflow_url = 'http://210.30.1.112:8089/Self/nav_getUserInfo'
        self.getdate_url = 'http://210.30.1.112:8089/Self/MonthPayAction.action'

        self.headers = {'Origin': 'http://210.30.1.112:8089',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0',
                        'Accept': 'image/webp,*/*;q=0.8',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Accept-Encoding': ' gzip,deflate,sdch',
                        'Referer': 'http://210.30.1.112:8089/Self/LogoutAction.action'
                        }

        self.s = requests.Session()


    def login(self):

        req = self.s.get(self.login_url)
        text = req.text
        checkcode = re.findall('var checkcode="(\d*)', text, re.S)
        self.s.get(self.random_url)


        self.postdata = {
                'account' : self.username,
                'password' : self.password,
                'code': '',
                'checkcode': checkcode[0],
                'Submit':'%E7%99%BB+%E5%BD%95'
                        }

        self.r = self.s.post(self.login_url, data = self.postdata)
        #return self.r.text
        if u'温馨提示' in self.r.text:
            return True
        else:
            return False

    def logout(self):
        try:
            req = self.s.get(self.logout_sessionid_url)
            text = req.text
            soup = BeautifulSoup(text)
            tag = soup.find('td', style = 'display:none;')
            sessionid = tag.string
            self.s.get(self.logout_url, params = {'t': '', 'fldsessionid': sessionid})
            status = u'下线成功'
            return status
        except AttributeError:
            status = u'账号处于离线状态'
            return status


    def get_flow(self):
        req = self.s.get(self.getflow_url)
        text = req.text
        soup = BeautifulSoup(text)
        tag = soup.find('td', text = re.compile(u"本月流量"))
        tag = tag.find_next_sibling('td')
        self.flow = string.strip(tag.string)

    def get_date(self):
        req = self.s.post(self.getdate_url, data = {'type': '1' ,'year': time.gmtime()[0]})
        text = req.text
        soup = BeautifulSoup(text)
        try:
            soup = soup.find('tbody').find('td').find_next_sibling('td')
            self.date = soup.string
        except AttributeError:  # if the date was Null
            self.date = u'不详'


    def deal_data(self):
        self.get_flow()
        self.get_date()
        flow_date = u'已使流量: %s MByte\n到期时间: %s'% (self.flow, self.date)
        return flow_date

