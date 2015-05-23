# coding=utf-8
import requests
import HTMLParser
import urlparse
import string
import re
import datetime
import json
from bs4 import BeautifulSoup

import sys
sys.path.append("..")
#from app import db
from models import Course, User_course


class urp:



    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
        self.courses_info_url = 'http://zhjw.dlnu.edu.cn/courseSearchAction.do'
        self.usercourse_url = 'http://zhjw.dlnu.edu.cn/xkAction.do?actionType=6'


        self.headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                'Accept': 'application/x-www-form-urlencoded',

                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=lnoper=fa'
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

    def usercourse(self):
        r = self.s.get(self.usercourse_url)
        soup = BeautifulSoup(r.text)
        courses = soup.find_all('img')
        for course in courses:
            course = str(course['name'])
            course = re.findall(r'\d{2,10}', course)  #using regex find the digit
            course_number = course[0]
            course_order = course[1]
            user_course = User_course(int(self.username), course_number, course_order)
            #db.session.add(user_course)
        #db.session.commit()


    def course_info(self):
        postdata = {
                'pageSize':'200000',
                'showColumn':[u'kch#课程号'.encode('gbk'), u'kcm#课程名'.encode('gbk'), u'kxh#课序号'.encode('gbk'), u'skjs#教师'.encode('gbk'), u'zcsm#周次'.encode('gbk'), u'skxq#星期'.encode('gbk'), u'skjc#节次'.encode('gbk'), u'xqm#校区'.encode('gbk'), u'jxlm#教学楼'.encode('gbk'), u'jasm#教室'.encode('gbk')],
                'pageNumber':'0',
                'actionType':'1'
                               }
        req = self.s.post(self.courses_info_url, postdata)
        soup= BeautifulSoup(req.text)
        courses = soup.find_all('tr', class_ = 'odd')
        for course in courses:
            course_number = course.find('td')
            course_name = course_number.find_next_sibling('td')
            course_order = course_name.find_next_sibling('td')
            weeks = course_order.find_next_sibling('td').find_next_sibling('td')
            day = weeks.find_next_sibling('td')
            time = day.find_next_sibling('td')
            school = time.find_next_sibling('td')
            building = school.find_next_sibling('td')
            classroom = building.find_next_sibling('td')
            weeks = weeks.string
            if len(weeks) > 1:    #skip the  courses which doesen't need go to class
                course_number = course_number.string
                course_name = course_name.string
                course_order = course_order.string
                day = day.string
                time = time.string
                if u'-' in weeks:
                    week = re.findall(r'\d{1,2}', weeks, re.X)
                    weeks =[]
                    for date in range(int(week[0]), int(week[1]) + 1):
                        weeks.append(str(date))
                else:
                    weeks = re.findall(r'\d{1,2}', weeks, re.X)
                weeks = json.dumps(weeks)

                if u'开发区' in school.string:        #checking which school
                    place = classroom.string
                else:
                    place = []
                    if building.string == classroom.string:  #skip the same name
                        place.append(classroom.string)
                    else:
                        place.append(building.string)
                        place.append(classroom.string)
                    place = ''.join(place)

                course = Course(course_number, course_name, course_order, weeks, day, time, place)
                db.session.add(course)
        db.session.commit()





