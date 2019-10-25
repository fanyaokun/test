from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Grade(db.Model):
    g_id = db.Column(db.Integer, primary_key=True)
    g_name = db.Column(db.String(20), unique=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student', backref='grade')

    __tablename__ = 'grade'


class Student(db.Model):
    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(16), unique=True)
    s_sex = db.Column(db.String(10))
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    __tablename__ = 'student'


class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(250))
    u_create_time = db.Column(db.DateTime, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('role.r_id'))

    __tablename__ = 'user'


class Role(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(10))
    users = db.relationship('User', backref='role')

    __tablename__ = 'role'


r_p = db.Table('r_p', db.Column('role_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True),
               db.Column('permission_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True))


class Permission(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(16), unique=True)
    p_er = db.Column(db.String(16), unique=True)
    roles = db.relationship('Role',secondary=r_p, backref=db.backref('permission', lazy=True))

    __tablename__ = 'permission'

