# coding=utf-8
import requests
import HTMLParser  
import urlparse  
import string  
import re  
import datetime 


class urp:

    

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.proxies = {
                  "http": "http://219.217.180.1:808"
                        }

        self.login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
        self.get_fulldata_url= 'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=603'
        self.get_recentdata_url= 'http://zhjw.dlnu.edu.cn/bxqcjcxAction.do'
        self.headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept': 'application/x-www-form-urlencoded',

                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
                        }  

        self.s = requests.Session()

        
    def login(self):
        self.postdata = {
                        'zjh' : self.username,
                        'mm' : self.password
                        }

        
        self.r = self.s.post(self.login_url, self.postdata, headers = self.headers)
        if len(self.r.text) == 489:
            return True
        else:
            return False
            
            

    def get_fulldata(self):
        self.k = self.s.get(self.get_fulldata_url, headers = self.headers)
        self.text = self.k.text
        garde =[]    
        items = re.findall('<tr.*?<td align="center">.*?<td align="center">.*?<td align="center">(.*?)</td>.*?<p align="center">(.+?)&nbsp;</P>.*?</td>.*?</tr>', self.text, re.S)
        if items == []:
            return u'无最近考试信息'
        else:
            for item in items:
                row = '%s  %s\n'% (string.strip(item[0]), string.strip(item[1]))
                garde.append(row)
            garde = ''.join(garde)
            return garde
            
    def get_recentdata(self):
        self.k = self.s.get(self.get_recentdata_url, headers = self.headers)
        self.text = self.k.text
        garde =[]    
        items = re.findall('<tr.*?<td align="center">.*?<td align="center">.*?<td align="center">(.*?)</td>.*?<p align="center">(.+?)&nbsp;</P>.*?</td>.*?</tr>', self.text, re.S)
        if items == []:
            return u'无最近考试信息'
        else:
            for item in items:
                row = '%s  %s\n'% (string.strip(item[0]), string.strip(item[1]))
                garde.append(row)
            garde = ''.join(garde)
            return garde

