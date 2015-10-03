#coding=utf-8

import traceback

from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for


from jinja2 import TemplateNotFound

from models import sysUser
from forms import adminForm
from login import login_required, after_login

from app import bcrypt
from app import db, app

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView

from app.education.models import Course, User_course
from app.user.models import regUser

from app.education.updata_user_courses import updata
from app.education.update_allCourse_single import updata_allCourses
from app.education.courses_lis import urp_courses

from gevent.monkey import patch_all
patch_all()

from gevent.pool import Pool
from time import time

manage = Blueprint('manage', __name__, template_folder = 'templates')

@manage.route('/admin_login', methods = ['POST','GET'])
@after_login
def manage_login():
    try:
        admin_form = adminForm()
        if admin_form.validate_on_submit():
            exist_user = sysUser.search_by_name(admin_form.username.data)

            if exist_user and bcrypt.check_password_hash(exist_user.password,
                                                          admin_form.password.data):
                session['user_id'] = exist_user.id

                return redirect(url_for('admin.index'))

            flash("Please check the username and password, and login again!")
        return render_template('admin.html',
                                form = admin_form
                                )
    except:
        traceback.print_exc()

@manage.route('/updata_courses')
@login_required
def update_courses():
    t1 = time()
    urp = urp_courses('2012081507','520134')
    if urp.login():
        urp.course_info()
    else:
        return '提供的用户名或密码错误！'
    t2 = time()
    return '用户课程更新成功\n用时:%fs'%(t2-t1)

@manage.route('/update_courses01')
@login_required
def update_courses_backup():
    courses = Course.query.all()    #update the  user's course info
    for data in courses:
        db.session.delete(data)
    t1 = time()
    allUser = regUser.query.all()
    pool = Pool(12)
    pool.map(updata_allCourses, [[user.username,user.password_urp]
                         for user in allUser]
                     )
    t2 = time()
    return '课程库更新成功，注意重复课程（请进数据库进行冗余操作）\n用时:%fs'%(t2-t1)


@manage.route('/update_user')
@login_required
def update_user():
    userCourses = User_course.query.all()    #update the  user's course info
    for data in userCourses:
        db.session.delete(data)
    t1 = time()
    allUser = regUser.query.all()
    pool = Pool(12)
    pool.map(updata, [[user.username,user.password_urp]
                         for user in allUser]
                     )
    t2 = time()
    return '用户课程更新成功\n用时:%fs'%(t2-t1)

class courseView(ModelView):
    page_size = 20  # the number of entries to display on the list view
    column_searchable_list = ['course_number' ,'course_name']

    def is_accessible(self):
        if 'user_id' in session.keys():
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('manage.manage_login'))

class userView(ModelView):
    can_create = False
    page_size = 20  # the number of entries to display on the list view
    column_searchable_list = ['username']

    def is_accessible(self):
        if 'user_id' in session.keys():
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('manage.manage_login'))

class userCourseView(ModelView):
    page_size = 20  # the number of entries to display on the list view
    column_searchable_list = ['course_number' ,'username']

    def is_accessible(self):
        if 'user_id' in session.keys():
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('manage.manage_login'))

class adminCourseView(ModelView):
    page_size = 20  # the number of entries to display on the list view

    def is_accessible(self):
        if 'user_id' in session.keys():
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('manage.manage_login'))

class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if 'user_id' not in session.keys():
            return redirect(url_for('manage.manage_login'))
        return self.render('admin_index.html')

    @expose('/logout/')
    def logout_view(self):
        """
        logout method, remove the user_id out of session.
        """
        session.pop('user_id', None)
        return redirect(url_for('user.index'))

admin = Admin(
                app, name = 'Wechat_Admin',
                index_view = MyAdminIndexView()
                )

admin.add_view(courseView(Course, db.session, name = u'课程库'))
admin.add_view(userCourseView(User_course, db.session, name = u'用户课程'))
admin.add_view(userView(regUser, db.session, name = u'学生信息'))
admin.add_view(adminCourseView(sysUser, db.session, name = u'管理员'))
