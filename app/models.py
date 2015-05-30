from app import db

class User(db.Model):
    #print "models imported as", __name__
    __table_args__ = {'extend_existing': True}
    __tablename__ = "user"
    openid = db.Column(db.String(80), primary_key = True)
    username = db.Column(db.Integer, unique=True)
    password_urp = db.Column(db.String(256))
    password_drcom = db.Column(db.String(256))

    def __init__(self, openid, username, password_urp, password_drcom):
        self.openid   = openid
        self.username = username
        self.password_urp = password_urp
        self.password_drcom = password_drcom

class Course(db.Model):
    #print "models imported as", __name__
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'course_info'
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String(80))
    course_name = db.Column(db.String(80))
    course_order = db.Column(db.String(80))
    weeks = db.Column(db.String(256))
    day = db.Column(db.String(80))
    time = db.Column(db.String(80))
    place = db.Column(db.String(256))

    def __init__(self, course_number, course_name, course_order, weeks, day, time, place):
        self.course_number = course_number
        self.course_name = course_name
        self.course_order = course_order
        self.weeks = weeks
        self.day = day
        self.time = time
        self.place = place

class User_course(db.Model):
    #print 'models imported as ', __name__
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'user_course'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer)
    course_number = db.Column(db.String(80))
    course_order = db.Column(db.String(80))

    def __init__(self, username, course_number, course_order):
        self.username = username
        self.course_number = course_number
        self.course_order = course_order

