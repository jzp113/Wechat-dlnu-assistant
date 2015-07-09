#coding=utf-8

from flask import render_template
from flask import flash
from flask import request
from flask import Flask
from flask import g
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for


from jinja2 import TemplateNotFound

from prphoto import bcrypt
from prphoto import db

from user.models import User
from utils.const import PASSWORD_KEYWORD
from utils.const import USER_KEY
from utils.login import login_required

profile = Blueprint('profile', __name__, template_folder = 'templates')

@admin.route('/admin/')

def my_profile():
    
    



