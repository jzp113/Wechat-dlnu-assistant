# coding=utf-8
import requests
from app import db
from models import User
from urp import urp
from book_list import book_list
from drcom import drcom

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
            geturp = urp(self.exist_user.username, self.exist_user.password_urp)
            if geturp.login():
                booklist = book_list(self.exist_user.username, self.exist_user.password_urp)
                booklist.login()
                booklist.get_data()
                booklist = booklist.deal_data()
                return booklist
            else:
                text = u'密码变化,请重新绑定'
                return text
            
    def binding(self):
        
        if self.exist_user is None:
            url = u'http://jzp113.ngrok.com/login?openid=' + self.fromuser
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
                text = u'密码变化,请重新绑定'
                return text

    def unlock(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            db.session.delete(self.exist_user)
            db.session.commit()
            text = u'解除绑定成功'
            return text

 
    def eggs(self):
        text = u'因鄙人极厌官僚之风，深恶校园各项业务之繁琐，书信不能达无奈出此下策，历时两月终出此作略有瑕疵望众海涵。于念逝去爱情，又鉴于民院帮手民大助手之粗俗，故得此名愿其永存于此      ————二流程序员书'
        return text

    def userguide(self):
        text = u'面板上的功能除了课表和图书都可以用了。查成绩有时候可能速度有点慢不过本人会努力优化的。另外求一名会python，一个人写好累啊（回复此平台即可）。'
        return text

    def key_check(self,key):
        lookup = {
            'binding': self.binding,
            'unlock': self.unlock,
            'drcom_logout': self.drcom_logout,
            'grade': self.recentgrade,
            'fullgrade':self.fullgrade,
            #'course':self.course,
            'book_list': self.booklist,
            'drcom_flow': self.drcom,
            'eggs': self.eggs,
            'userguide': self.userguide
         }
        lookup.get(key, lambda: None)()
        func = lookup[key]
        return func()
         

