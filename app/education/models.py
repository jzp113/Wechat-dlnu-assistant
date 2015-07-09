from app import db

class Course(db.Model):
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
    __tablename__ = 'user_course'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer)
    course_number = db.Column(db.String(80))
    course_order = db.Column(db.String(80))

    def __init__(self, username, course_number, course_order):
        self.username = username
        self.course_number = course_number
        self.course_order = course_order

