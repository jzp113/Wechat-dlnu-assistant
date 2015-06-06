# -*- coding: utf-8 -*-
import requests
import HTMLParser
import urlparse
import string
import re
import datetime
from bs4 import BeautifulSoup
import random
from multiprocessing.dummy import Pool
import time
from datetime import datetime, date

class urp:


    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.proxies = {
                  "http": "http://127.0.0.1:8080"
                        }

        self.login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
        self.get_fulldata_url= 'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
        self.get_recentdata_url= 'http://zhjw.dlnu.edu.cn/bxqcjcxAction.do'

        self.get_evaluation_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=listWj'
        self.open_evaluation_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do'
        self.post_evaluation_data_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=wjpg'

        self.getTestInfo_url = 'http://zhjw.dlnu.edu.cn/ksApCxAction.do?oper=getKsapXx'

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

    #def post_evaluation(self, wjbm, bpr, pgnr):
    def post_evaluation(self, lists):
        data = {}
        evaluation_data = {}
        wjbm = lists[0]
        bpr = lists[1]
        pgnr = lists[2]
        #self.wjbm = wjbm
        #self.bpr = bpr
        #self.pgnr = pgnr
        postdata = {
                    'wjbm':wjbm,
                    'bpr': bpr,
                    'pgnr':pgnr,
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
            #evaluation_data[key] = random.choice(value)
            evaluation_data[key] = value[random.randint(0,1)]
        evaluation_data['wjbm'] = wjbm
        evaluation_data['bpr'] = bpr
        evaluation_data['pgnr'] = pgnr
        evaluation_string = u'''悔人不倦 废寝忘食 埋头苦干 兢兢业业 尽心尽力
        一丝不苟 文思敏捷 聪明过人 青出于蓝 一鸣惊人 桃李争妍 后继有人
        默默无闻 孜孜不倦 德才兼备 春风化雨 润物无声 循循善诱 潜移默化
        和蔼可亲 无微不至 勤勤恳恳 良师益友 桃李芬芳 教导有方 辛勤劳碌 教无常师 
        良师益友 能者为师 青出于蓝 师道尊严 研桑心计 一字之师 尊师重道 春风化雨 
        蜡炬成灰泪始干 循循善诱 诲人不倦 桃李满天下 桃李满门 先圣先师 良工心苦 门墙桃李
        教导有方 默默无闻 孜孜不倦 德才兼备 呕心沥血 披星戴月 循循善诱 因材施教 师道尊严
        教无常师 良师益友 能者为师 青出于蓝 师道尊严
        研桑心计 一字之师 尊师重道 春风化雨 呕心沥血
        蜡炬成灰泪始干 循循善诱 诲人不倦 桃李满天下
        桃李满门 先圣先师 良工心苦 门墙桃李 良师出高徒
        鞠躬尽瘁 诲人不倦 良师益友 师道尊严 教导有方
        默默无闻 孜孜不倦 德才兼备 辛勤劳碌'''.encode('gbk')
        evaluation_list = re.findall('[\x80-\xff]{8}',evaluation_string)
        text = random.choice(evaluation_list)
        evaluation_data['zgpj'] = text.strip()
        self.s.post(self.post_evaluation_data_url, data = evaluation_data)

    def evaluation(self):
        lists = []
        req = self.s.get(self.get_evaluation_url)
        text = req.text
        soup= BeautifulSoup(text)
        soup = soup.find_all('img', align = "center")
        for litem in soup:
            data = []
            s =  litem['name'].split('#@')
            data.append(s[0])
            data.append(s[1])
            data.append(s[-1])
            lists.append(data)
        return lists

    def testInfo(self):
        test_list = []
        format_test_list = []
        #test_list = [u'|科目|教室|日期|时间|座位号|']
        req = self.s.get(self.getTestInfo_url)
        soup = BeautifulSoup(req.text)
        testlist = soup.find_all('tr', class_ ='odd')
        if testlist == []:
            return u'暂无考试信息'
        else:
            for testdata in testlist:
                testSchool = testdata.find('td').find_next_sibling('td')
                testBulding = testSchool.find_next_sibling('td')
                testRoom = testBulding.find_next_sibling('td')
                testName = testRoom.find_next_sibling('td')
                testDate = testRoom.find_next('td').find_next('td')
                testTime = testDate.find_next('td')
                testSeat = testTime.find_next('td')
                format_testDate = datetime.strptime(testDate.string, '%Y-%m-%d').date()
                if date.today() > format_testDate:
                    pass
                else:
                    if u'开发区' in testSchool.string:
                        testPlace = testRoom.string
                    else:
                        testPlace = testBulding.string + testRoom.string
                    '''
                    data = u'科目: %s\n教室: %s\n日期: %s\n时间: %s\n座位: %s'%(testName.string.strip(), testPlace,\
                                            format_testDate, testTime.string,\
                                            testSeat.string )
                    '''
                    data = [testName.string.strip(), testPlace, format_testDate,
                            testTime.string, testSeat.string]
                    test_list.append(data)

        if len(test_list) > 0:
            test_list.sort(key=lambda date : date[2])
            for data in test_list:
                test_str = u'科目: %s\n教室: %s\n日期: %s\n时间: %s\n座位: %s'\
                            %(data[0] ,data[1] ,data[2], data[3], data[4])
                format_test_list.append(test_str)
            format_testStr = '\n\n'.join(format_test_list)
            return format_testStr

        else:
            return u'暂无考试信息'

#if __name__ =='__main__':
#    userid = '2014022416'
#    passwd = '123456'
#    #userid = '2012081507'
#    #passwd = '520134'
#    urp = urp(userid, passwd)
#    if urp.login():
#        print urp.testInfo()
#        '''
#        start = time.time()
#        lists = urp.evaluation()
#        pool = Pool(12)
#        pool.map(urp.post_evaluation, lists)
#        pool.close()
#        pool.join()
#        end = time.time()
#        print 'using time %s' %(end - start)
#        '''
#    else:
#        print 'invalid passwd'
#
