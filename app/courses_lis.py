# coding=utf-8
import requests
import HTMLParser
import urlparse
import string
import re
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup

import sys
sys.path.append("..")
from app import db
from models import Course, User_course, User

from sqlalchemy import text


class urp_courses:



    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
        self.courses_info_url = 'http://zhjw.dlnu.edu.cn/courseSearchAction.do'
        self.usercourse_url = 'http://zhjw.dlnu.edu.cn/xkAction.do?actionType=6'

        self.getweek_url = 'http://210.30.1.19/mhpd/xl.jsp'

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
        if len(r.text) < 888:
            return True
        else:
            return False

    def usercourse(self):
        datas = User_course.query.filter_by(username=self.username).all()    #update the  user's course info
        if datas != []:
            for data in datas:
                db.session.delete(data)
        r = self.s.get(self.usercourse_url)
        soup = BeautifulSoup(r.text)
        courses = soup.find_all('img')
        if courses != []:
            for course in courses:
                sign = course.find_next('td').find_next('td').find_next('td')
                if len(sign.string) > 1:
                    course = str(course['name'])
                    course = re.findall(r'kch=(.*?)&kxh=(\d+)', course)  #using regex find the digit
                    course_number = course[0][0]
                    course_order = course[0][1]
                    user_course = User_course(int(self.username), course_number, course_order)
                    db.session.add(user_course)
        db.session.commit()

    def course_info(self):
        courses = Course.query.all()
        for course in courses:
            db.session.delete(course)
        postdata = {
                'pageSize':'200000',
                'showColumn':[u'kch#课程号'.encode('gbk'),
                              u'kcm#课程名'.encode('gbk'),
                              u'kxh#课序号'.encode('gbk'),
                              u'skjs#教师'.encode('gbk'),
                              u'zcsm#周次'.encode('gbk'),
                              u'skxq#星期'.encode('gbk'),
                              u'skjc#节次'.encode('gbk'),
                              u'xqm#校区'.encode('gbk'),
                              u'jxlm#教学楼'.encode('gbk'),
                              u'jasm#教室'.encode('gbk')],
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
            weeks = weeks.string.strip()
            if len(weeks) > 1:    #skip the  courses which doesen't need go to class
                course_number = course_number.string.strip()
                course_name = course_name.string.strip()
                course_order = course_order.string.strip()
                day = day.string.strip()
                time = time.string.strip()
                week = re.findall(r'\d{1,2}', weeks, re.X)
                if u'-' in weeks:
                    firstWeek = int(week[0])
                    lastWeek = int(week[1])
                    gap = 2
                    if u'单' in weeks:
                        pass
                    elif u'双' in weeks:
                        firstWeek += 1
                    else:
                        gap = 1
                    weeks = [str(week) for week in range(firstWeek,lastWeek+1,gap)]
                else:
                    weeks = week
                weeks = json.dumps(weeks)

                if u'开发区' in school.string:        #checking which school
                    place = classroom.string.strip()
                else:
                    if building.string == classroom.string:  #skip the same name
                        place = [classroom.string.strip()]
                    else:
                        place = [building.string.strip(),classroom.string.strip()]
                    place = ''.join(place)
                course = Course(course_number, course_name, course_order, weeks, day, time, place)
                db.session.add(course)
        db.session.commit()


    def CheckMaxTime(self, key):   #set the maxtime of the course time
        maxtime = {
                '1':'9',
                '3':'11',
                '5':'14',
                '7':'16',
                '9':'19'
                }
        time = maxtime[key]
        return time

    def db_courses(self, day):
        results = db.session.query('course_name', 'weeks', 'time', 'place').\
        from_statement(text(
        '''SELECT  course_info.course_name,  weeks, day, time, place
        FROM course_info, user_course
        WHERE course_info.course_number = user_course.course_number
        AND course_info.course_order = user_course.course_order
        AND username = :username
        AND day = :day
        ORDER BY time ASC''')).params(username = self.username, day = str(day)).all()
        return results

    def get_courses(self):
        r = requests.get(self.getweek_url)
        soup = BeautifulSoup(r.text)
        week = soup.find('font', size='6')
        self.week = week.string

        if self.week > u'20':
            return u'童鞋，放假了啦'

        else:
            today = datetime.today().isoweekday()
            results = self.db_courses(today)
            if datetime.now().hour >= 20:   #output tomorrow courses
                return self.tomorrow_courses()

            elif results == []:
                return u'童鞋没课哦'

            else:
                data = [u'-----------------------------------',
                        u'|--节次--|---课程---|--教室---|']
                for result in results:
                    weeks = json.loads(result.weeks)
                    if self.week in weeks:
                        MaxHour = int(self.CheckMaxTime(result.time))
                        if datetime.now().hour < MaxHour:
                            row = u'|%s-%s|%s|%s|'%(result.time,str(int(result.time)+1), result.course_name, result.place)
                            data.append(row)
                if len(data) > 2:
                    courseText = '\n'.join(data)
                    return courseText
                else:
                    return u'童鞋没课了哦'

    def tomorrow_courses(self):
        tomorrow = datetime.today() + timedelta(days=1)
        tomorrow = tomorrow.isoweekday()
        if tomorrow == 1:
            NextWeek = str(int(self.week) + 1)
        else:
            NextWeek = self.week
        results = self.db_courses(tomorrow)
        if results == []:
            return  u'童鞋明天没课哦，放心的睡吧!'
        else:
            data = [u'-----------------------------------',
                    u'|--节次--|---课程---|--教室---|']
            for result in results:
                weeks = json.loads(result.weeks)
                if NextWeek in weeks:
                    row = u'|%s-%s|%s|%s|'%(result.time, str(int(result.time)+1), result.course_name, result.place)
                    data.append(row)
            if len(data) > 2:
                courseText = '\n'.join(data)
                return courseText
            else:
                return u'童鞋明天没课哦，放心的睡吧!'

if __name__ == '__main__':
    userid = '2013064115'
    passwd = '6845705'
    #user = User.query.filter_by(username=userid).first()
    #print user.username,user.password_urp
    #print type(user.username),type(user.password_urp)
    urp = urp_courses(userid, passwd)
    if urp.login():
        #urp.course_info()
        #datas = urp.db_courses(1)
        #for data in datas:
            #print data.course_name,data.time
        urp.usercourse()
        #print urp.get_courses()
    else:
        print 'invaild passwd'
