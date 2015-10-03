from app import db

class sysUser(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(256))

    def __init__(self, username='', password=''):
        self.username = username
        self.password = password

    @classmethod
    def search_by_name(cls, name):
        return db.session.query(cls).filter(cls.username == name).first()

    @classmethod
    def get_user_by_id(cls, user_id):
        return db.session.query(cls).get(user_id)
