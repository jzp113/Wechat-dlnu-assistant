# -*- coding: utf-8 -*-

from flask import render_template
from flask import flash
from flask import request
from flask import Blueprint
from flask import redirect
from flask import url_for

from app import db

from forms import LoginForm, EvaluationForm
from models import User

from app.education.urp import urp
from app.education.courses_lis import urp_courses
from app.education.updata_user_courses import updata

from multiprocessing.dummy import Pool

from gevent.monkey import patch_all
patch_all()
from psycogreen.gevent import patch_psycopg
patch_psycopg()

from gevent.pool import Pool as gPool

from time import time

user = Blueprint('user', __name__, template_folder = 'templates')

@user.route('/fuck', methods = ['GET','POST'])
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


@user.route('/')
@user.route('/index')
def index():
    return render_template('index.html')

@user.route('/test')
def test():
    urp = urp_courses('2012081507','520134')
    if urp.login():
        urp.course_info()
    else:
        flash('passwd error!')
    return 'succeed'

@user.route('/updata_user')
def updata_user():
    t1 = time()
    allUser = User.query.all()
    pool = gPool(12)
    pool.map(updata, [[user.username,user.password_urp]
                         for user in allUser]
                     )
    t2 = time()
    return 'succeed \n run:%f'%(t2-t1)



@user.route('/login', methods = ['GET', 'POST'])
def login():
    openid = request.args.get('openid', '')
    form = LoginForm()
    if form.validate_on_submit() and openid:
        if User.query.filter_by(username = form.username.data).first() \
        or User.query.filter_by(openid = openid).first():
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


