import os
import sys

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

def register_blueprints():

    from app.user.views import user
    from app.weixin.views import weixin

    app.register_blueprint(user)
    app.register_blueprint(weixin)

register_blueprints()
