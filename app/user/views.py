# -*- coding: utf-8 -*-

from flask import render_template
from flask import flash
from flask import request
from flask import Blueprint
from flask import redirect
from flask import url_for

from app import db

from forms import LoginForm, EvaluationForm
from models import regUser

from app.education.urp import urp

from multiprocessing.dummy import Pool

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

@user.route('/login', methods = ['GET', 'POST'])
def login():
    openid = request.args.get('openid', '')
    form = LoginForm()
    if form.validate_on_submit() and openid:
        if regUser.query.filter_by(username = form.username.data).first() \
        or regUser.query.filter_by(openid = openid).first():
            flash('用户只能绑定一次')
        elif urp(form.username.data, form.password_urp.data).login():
            user = regUser(openid, form.username.data, form.password_urp.data, form.password_drcom.data)
            db.session.add(user)
            db.session.commit()
            return render_template('succeed.html')
        else:
            flash("用户名或密码错误")
    return render_template('login1.html',
        title = 'Sign In',
        form = form)


