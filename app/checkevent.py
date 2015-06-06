# coding=utf-8
import requests
from app import db
from models import Course, User_course, User
from urp import urp
#from book_list import book_list
from newbook_list_httpRequestVersion import book_list
from drcom import drcom
from courses_lis import urp_courses

class checkevent:
    def __init__(self, fromuser):

        self.fromuser = fromuser
        self.exist_user = User.query.filter_by(openid = self.fromuser).first()


    def recentgrade(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            geturp = urp(self.exist_user.username, self.exist_user.password_urp)
            if geturp.login():
                grades = geturp.get_recentdata()
                return grades
            else:
                text = u'密码变化,请重新绑定'
                return text

    def testinfo(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            geturp = urp(self.exist_user.username, self.exist_user.password_urp)
            if geturp.login():
                text = geturp.testInfo()
                return text
            else:
                text = u'密码变化,请重新绑定'
                return text

    def fullgrade(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            geturp = urp(self.exist_user.username, self.exist_user.password_urp)
            if geturp.login():
                grades = geturp.get_fulldata()
                return grades
            else:
                text = u'密码变化,请重新绑定'
                return text

    def booklist(self):

        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            booklist = book_list(self.exist_user.username)
            booklist.login()
            booklist = booklist.get_booklists()
            return booklist

    def delay_return(self):

        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            delaybook = book_list(self.exist_user.username)
            delaybook.login()
            delaybook = delaybook.delay_return()
            return delaybook

    def course(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            getCourse = urp_courses(self.exist_user.username, self.exist_user.password_urp)
            if getCourse.login():
                data = getCourse.get_courses()
                return data
            else:
                text = u'密码变化,请重新绑定'
                return text

    def updatecourses(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            getCourse = urp_courses(self.exist_user.username, self.exist_user.password_urp)
            if getCourse.login():
                getCourse.usercourse()
                return  u'课程更新成功'
            else:
                text = u'密码变化,请重新绑定'
                return text


    def binding(self):

        if self.exist_user is None:
            url = u'http://219.217.179.16/login?openid=' + self.fromuser
            href = u'<a href="%s">点我绑定</a>' %url
            return href

        else:
            text = u'您已绑定,如密码变化,请先解除绑定.'
            return text

    def drcom(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            getdrcom= drcom(self.exist_user.username, self.exist_user.password_drcom)
            if getdrcom.login():
                getdrcom.get_flow()
                getdrcom.get_date()
                flow_date = getdrcom.deal_data()
                return flow_date
            else:
                text = u'密码变化,请重新绑定'
                return text

    def drcom_logout(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            getdrcom= drcom(self.exist_user.username, self.exist_user.password_drcom)
            if getdrcom.login():
                text = getdrcom.logout()
                return text
            else:
                status = u'密码变化,请重新绑定'
                return status

    def unlock(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            db.session.delete(self.exist_user)
            db.session.commit()
            text = u'解除绑定成功'
            return text

    def codeinfo(self):
        text = u'因鄙人极厌官僚之风，深恶校园各项业务之繁琐，书信不能达无奈出此下策，历时两月终出此作略有瑕疵望众海涵。于念逝去之爱情，又鉴于民院帮手民大助手之粗俗，故得此名愿其永存于此      ————二流程序员书'
        return text

    def eggs(self):
        text = u"猜猜我是不是帅哥，答对有奖O(∩_∩)O"
        return text

    def userguide(self):
        text = u'我写的还不够傻瓜吗？(*^__^*) 嘻嘻……just a joke'
        return text

    def subscribe(self):
        text = u'''同学欢迎使用民院小偲(*^__^*)\n
                    使用教程：\n
                    （一）点击账户，绑定用户\n
                    （二）点击账户，课程更新\n
                    Tips：\n
                        超过晚上8点，点击课表助手推送为第二天课表\n
                        课表信息错误时，请点击课程更新\n
                    当遇到什么问题后者bug回复即可，小编一定会第一时间帮你解决'''
        return text

    def key_check(self,key):
        lookup = {
            'binding': self.binding,
            'unlock': self.unlock,
            'updatecourses':self.updatecourses,
            'drcom_logout': self.drcom_logout,
            'grade': self.recentgrade,
            'fullgrade':self.fullgrade,
            'testinfo':self.testinfo,
            'course':self.course,
            'book_list': self.booklist,
            'delaybook': self.delay_return,
            'drcom_flow': self.drcom,
            'codeinfo':self.codeinfo,
            'eggs': self.eggs,
            'userguide': self.userguide,
            'subscribe':self.subscribe
         }
        lookup.get(key, lambda: None)()
        func = lookup[key]
        return func()


