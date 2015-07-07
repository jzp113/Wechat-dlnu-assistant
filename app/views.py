# coding=utf-8
from flask import render_template
from flask import flash
from flask import request
from flask import Flask
from flask import g
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for
from flask import escape

from app import app
from app import db

from forms import LoginForm, EvaluationForm
from models import User


from urp import urp
from checkevent import checkevent
from courses_lis import urp_courses

from multiprocessing.dummy import Pool

import urllib
import urllib2
from urllib import urlencode
import json
import time
import hashlib
import xml.etree.ElementTree as ET

@app.route('/fuck', methods = ['GET','POST'])
def evalution():
    form = EvaluationForm()
    if form.validate_on_submit():
        fuck_dlnu = urp(form.username.data, form.password_urp.data)
        if fuck_dlnu.login():
            lists = fuck_dlnu.evaluation()
            pool = Pool(12)
            pool.map(fuck_dlnu.post_evaluation, lists)
            pool.close()
            pool.join()
            return redirect('/')
        flash("密码输入有误")
    return render_template('evaluation.html',
        title = 'Fuckin School',
        form = form)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    urp = urp_courses('2012081507','520134')
    if urp.login():
        urp.course_info()
        flash('succeed!')
    else:
        flash('fail!')
    return render_template('succeed.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    openid = request.args.get('openid', '')
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(username = form.username.data).first() is not None \
        or User.query.filter_by(openid = openid).first() is not None:
            flash('用户只能绑定一次')
        elif urp(form.username.data, form.password_urp.data).login():
            user = User(openid, form.username.data, form.password_urp.data, form.password_drcom.data)
            db.session.add(user)
            db.session.commit()
            return render_template('succeed.html')
        else:
            flash("用户名或密码错误")
    return render_template('login1.html',
        title = 'Sign In',
        form = form)

@app.route('/weixin',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='jzp113'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        event = xml_rec.find('Event')
        event_key = xml_rec.find('EventKey')
        content = xml_rec.find('Content')

        if content is not None:
            contents = chatApi(content.text)
        elif event.text == 'subscribe':
            key = 'subscribe'
            contents = checkevent(fromu).key_check(key)
        else:
            key = event_key.text
            contents = checkevent(fromu).key_check(key)


        return render_template('reply_text.xml',
        toUser = fromu,
        fromUser = tou,
        createtime = str(int(time.time())),
        content = contents
        )

