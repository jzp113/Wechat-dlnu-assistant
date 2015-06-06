#encoding:utf-8
import requests
import HTMLParser
import urlparse
import string
import re
import datetime
from bs4 import BeautifulSoup

class book_list:

    def __init__(self, username):

        self.username = username


        self.login_url = 'http://210.30.8.167:8080/reader/hwthau3.php'
        self.delay_url= 'http://210.30.8.167:8080/reader/ajax_renew.php'

        self.headers = {#'Host': 'portal.dlnu.edu.cn',
                        #'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0',
                        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        #'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        }

        self.s = requests.Session()

    def login(self):

        payload = {'userid':self.username}

        req = self.s.get(self.login_url, params = payload)
        self.text = req.content.decode('utf8')


    def get_booklists(self):

        book = []
        soup = BeautifulSoup(self.text)
        sign = soup.find(class_ = 'whitetext')

        if sign == None:

            return u'无借阅信息'

        else:
            bookcontent = soup.find('tr').find_all_next('tr')
            for booklist in bookcontent:
                bookname = booklist.find('a').string
                returndate = booklist.find('font').string
                row = u'%s\n到期时间: %s'%(bookname, returndate)
                book.append(row)
            book = '\n'.join(book)
            return book

    def delay_return(self):
        meg = []
        soup = BeautifulSoup(self.text)
        sign = soup.find(class_ = 'whitetext')

        if sign == None:

            return u'无借阅信息'

        else:
            bookcontent = soup.find('tr').find_all_next('tr')
            for booklist in bookcontent:
                bookname = booklist.find('a').string
                data = booklist.find('input')
                data = data['onclick'].split("'")
                barcode = data[1]
                checkcode = data[3]
                payload = {'bar_code':barcode, 'check':checkcode}
                req = self.s.get(self.delay_url, params = payload)
                req = req.content.decode('utf8')
                if u'red' in req:
                    row = u'%s 未到续期条件'%(bookname)
                else:
                    row = u'%s 续借成功'%(bookname)
                meg.append(row)
            meg = '\n'.join(meg)
            return meg





