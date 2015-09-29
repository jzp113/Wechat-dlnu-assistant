# -*- coding: utf-8 -*-
import requests
import string
import re
import json
from bs4 import BeautifulSoup

from app import db
from models import Course

def updata_allCourses(lists):

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
    if len(r.text) < 888:     #get all courses info  from every user
        r = s.get(usercourse_url)
        soup = BeautifulSoup(r.text, 'lxml')
        courses = soup.find_all('tr', class_ = 'odd')
        for x in xrange(len(courses)):
            rowSign = courses[x].find('td', rowspan=True)
            if rowSign:
                row =  int(rowSign['rowspan'])
                for i in xrange(x,x+row):
                    if i == x:
                        cNum =  courses[x].find('td').find_next('td')
                        cName = cNum.find_next('td')
                        cOrd =  cName.find_next('td')
                        cWeeks = courses[i].find('img').find_next('td').\
                        find_next('td').find_next('td')
                        cDay = cWeeks.find_next('td')
                        cTime = cDay.find_next('td')
                        cSchool = cTime.find_next('td').find_next('td')
                        cBuilding = cSchool.find_next('td')
                        cRoom = cBuilding.find_next('td')

                        cNum = cNum.string.strip()
                        cName = cName.string.strip()
                        cOrd = cOrd.string.strip()
                        cDay = cDay.string.strip()
                        cTime = cTime.string.strip()
                        cWeeks = cWeeks.string.strip()
                        all_weeks = []
                        week_date = cWeeks.split(',')
                        for date in week_date:
                            week = re.findall(r'\d{1,2}', date, re.X)
                            if u'-' in date:
                                firstWeek = int(week[0])
                                lastWeek = int(week[1])
                                gap = 2
                                if u'单' in cWeeks:
                                    pass
                                elif u'双' in cWeeks:
                                    firstWeek += 1
                                else:
                                    gap = 1
                                weeks = [str(week) for week in range(firstWeek,lastWeek+1,gap)]
                            else:
                                weeks = week
                            all_weeks.extend(weeks)
                        weeks = json.dumps(all_weeks)

                        if u'开发区' in cSchool.string:        #checking which school
                            place = cRoom.string.strip()
                        else:
                            if cBuilding.string == cRoom.string:  #skip the same name
                                place = [cRoom.string.strip()]
                            else:
                                place = [cBuilding.string.strip(),cRoom.string.strip()]
                            place = ''.join(place)

                    else:
                        cNum =  courses[x].find('td').find_next('td')
                        cName = cNum.find_next('td')
                        cOrd =  cName.find_next('td')
                        cWeeks = courses[i].find('td')
                        cDay = cWeeks.find_next('td')
                        cTime = cDay.find_next('td')
                        cSchool = cTime.find_next('td').find_next('td')
                        cBuilding = cSchool.find_next('td')
                        cRoom = cBuilding.find_next('td')

                        cNum = cNum.string.strip()
                        cName = cName.string.strip()
                        cOrd = cOrd.string.strip()
                        cDay = cDay.string.strip()
                        cTime = cTime.string.strip()
                        cWeeks = cWeeks.string.strip()
                        all_weeks = []
                        week_date = cWeeks.split(',')
                        for date in week_date:
                            week = re.findall(r'\d{1,2}', date, re.X)
                            if u'-' in date:
                                firstWeek = int(week[0])
                                lastWeek = int(week[1])
                                gap = 2
                                if u'单' in cWeeks:
                                    pass
                                elif u'双' in cWeeks:
                                    firstWeek += 1
                                else:
                                    gap = 1
                                weeks = [str(week) for week in range(firstWeek,lastWeek+1,gap)]
                            else:
                                weeks = week
                            all_weeks.extend(weeks)
                        weeks = json.dumps(all_weeks)

                        if u'开发区' in cSchool.string:        #checking which school
                            place = cRoom.string.strip()
                        else:
                            if cBuilding.string == cRoom.string:  #skip the same name
                                place = [cRoom.string.strip()]
                            else:
                                place = [cBuilding.string.strip(),cRoom.string.strip()]
                            place = ''.join(place)

                    course = Course(cNum, cName, cOrd, weeks, cDay, cTime, place)
                    db.session.add(course)
        db.session.commit()

