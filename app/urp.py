# coding=utf-8
import requests
import HTMLParser  
import urlparse  
import string  
import re  
import datetime 
from bs4 import BeautifulSoup
import random


class urp:

    

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.proxies = {
                  "http": "http://219.217.180.1:808"
                        }

        self.login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
        self.get_fulldata_url= 'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
        self.get_recentdata_url= 'http://zhjw.dlnu.edu.cn/bxqcjcxAction.do'
        
        self.get_evaluation_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=listWj'
        self.open_evaluation_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do'
        self.post_evaluation_data_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=wjpg'
        
        self.headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept': 'application/x-www-form-urlencoded',

                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
                        }  

        self.s = requests.Session()

        
    def login(self):
        postdata = {
                        'zjh' : self.username,
                        'mm' : self.password
                        }

        
        r = self.s.post(self.login_url, postdata, headers = self.headers)
        if len(r.text) == 489:
            return True
        else:
            return False
            
            

    def get_fulldata(self):
        req = self.s.get(self.get_fulldata_url)
        text = req.text
        soup = BeautifulSoup(text)
        tag = soup.find('iframe')
        url_fulldata = 'http://zhjw.dlnu.edu.cn/' + tag['src']
        req = self.s.get(url_fulldata)
        text = req.text
        garde =[]
        items = re.findall('<tr.*?<td align="center">.*?<td align="center">.*?<td align="center">(.*?)</td>.*?<p align="center">(.+?)&nbsp;</P>.*?</td>.*?</tr>', text, re.S)
        if items == []:
            return u'无最近考试信息'
        else:
            for item in items:
                row = u'%s  %s'% (string.strip(item[0]), string.strip(item[1]))
                garde.append(row)
            garde = '\n'.join(garde)
            return garde




    def get_recentdata(self):
        data = []
        req = self.s.get(self.get_recentdata_url, headers = self.headers)
        text = req.text
        soup = BeautifulSoup(text)
        courses = soup.find_all('tr', onmouseout="this.className='even';")
        if courses == []:
            return u'无最近考试信息'
        else:
            for course in courses:
                name = course.find('td').find_next_sibling('td').find_next_sibling('td')
                grade = name.find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td')
                name = string.strip(name.string)
                grade = string.strip(grade.string)
                if len(grade) != 0:
                    row = u'%s  %s'% (name, grade)
                    data.append(row)
            data = '\n'.join(data)
            if  len(data) == 0:
                return u'无最近考试成绩'
            else:
                return data

    def post_evaluation(self, wjbm, bpr, pgnr):
        data = {}
        evaluation_data = {}
        self.wjbm = wjbm
        self.bpr = bpr
        self.pgnr = pgnr
        postdata = {
                    'wjbm': self.wjbm,
                    'bpr': self.bpr,
                    'pgnr': self.pgnr,
                    'oper': 'wjShow',
                    'wjmc': '',
                    'bprm': '',
                    'pgnrm': '',
                    'pageSize': '20',
                    'page': '1',
                    'currentPage': '1',
                    'pageNo': ''
                    }
        r = self.s.post(self.open_evaluation_url, data = postdata)
        soup = BeautifulSoup(r.text)
        orders = soup.find_all(type='radio')
        for order in orders:
            key = order['name']
            value = order['value']
            if key in data:
                data[key].append(value)
            else:
                data[key] = [value]     #make dict like that  {'key':[value0,value1]}
        for key, value in data.items():
            evaluation_data[key] = random.choice(value)
        evaluation_data['wjbm'] = self.wjbm
        evaluation_data['bpr'] = self.bpr
        evaluation_data['pgnr'] = self.pgnr
        evaluation_data['zgpj'] = u'认真仔细'.encode('gbk')
        self.s.post(self.post_evaluation_data_url, data = evaluation_data)

    def evaluation(self):

        req = self.s.get(self.get_evaluation_url)
        text = req.text
        soup= BeautifulSoup(text)
        soup = soup.find_all('img', align = "center")
        for litem in soup:
            s =  litem['name'].split('#@')
            self.post_evaluation(s[0], s[1], s[-1])
            #self.open_evaluation(s[0], s[1], s[-1])
            #self.postevaluation()

if __name__ =='__main__':
    userid = '2012081507'
    passwd = '520134'
    urp = urp(userid, passwd)
    if urp.login():
        urp.evaluation()
    else:
        print 'invalid passwd'
