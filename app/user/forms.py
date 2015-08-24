
from flask.ext.wtf import Form
from wtforms import TextField, IntegerField,PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    username = IntegerField('username', validators = [Required()])
    password_urp = PasswordField('password_urp', validators = [Required()])
    password_drcom = PasswordField('password_drcom', validators = [Required()])

class EvaluationForm(Form):
    username = TextField('username', validators = [Required()])
    password_urp = PasswordField('password_urp', validators = [Required()])
