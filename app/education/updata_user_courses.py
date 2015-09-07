# -*- coding: utf-8 -*-
import requests
import string
import re
from bs4 import BeautifulSoup

from app import db
from models import User_course

def updata(lists):

    login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
    usercourse_url = 'http://zhjw.dlnu.edu.cn/xkAction.do?actionType=6'

    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                'Accept': 'application/x-www-form-urlencoded',
                'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                'Accept-Encoding':    'gzip, deflate',
                'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=lnoper=fa'
                }

    s = requests.Session()


    postdata = {
                    'zjh' : lists[0],
                    'mm' : lists[1]
                    }


    r = s.post(login_url, postdata, headers = headers)
    if len(r.text) < 888:
        datas = User_course.query.filter_by(username=lists[0]).all()    #update the  user's course info
        if datas:
            for data in datas:
                db.session.delete(data)
        req = s.get(usercourse_url)
        soup = BeautifulSoup(req.text)
        courses = soup.find_all('img')
        if courses:
            for course in courses:
                sign = course.find_next('td').find_next('td').find_next('td')
                if len(sign.string) > 1:
                    course = str(course['name'])
                    course = re.findall(r'kch=(.*?)&kxh=(\d+)', course)  #using regex find the digit
                    course_number = course[0][0]
                    course_order = course[0][1]
                    user_course = User_course(int(lists[0]), course_number, course_order)
                    db.session.add(user_course)
        db.session.commit()
