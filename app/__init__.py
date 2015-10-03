import os
import sys

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt



app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
db.engine.pool._use_threadlocal = True

def register_blueprints():

    from app.user.views import user
    from app.weixin.views import weixin
    from app.admin.views import manage

    app.register_blueprint(user)
    app.register_blueprint(weixin)
    app.register_blueprint(manage)

register_blueprints()
