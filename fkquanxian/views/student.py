from flask import Blueprint,render_template,request,jsonify,session,redirect
from sqlalchemy import false

from models.models import Grade,Student
from utils.decorator import is_login
from models.models import db

student = Blueprint('student', __name__)

# 学生列表
@student.route('/student/')
@is_login
def _student():
    page = int(request.args.get('page', 1))
    paginate = Student.query.paginate(page, 2, error_out=false)
    return render_template('student.html', paginate=paginate)

# 删除学生
@student.route('/deletestu/<id>')
@is_login
def delete(id):
    student = Student.query.filter(Student.s_id == id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect('/user/student/')

# 添加学生
@student.route('/addstu/', methods=['post','get'])
@is_login
def addstu():
    grades = Grade.query.all()
    if request.method == 'GET':
        students = Student.query.all()
        return render_template('addstu.html', students=students, grades=grades)
    if request.method == 'POST':
        s_name = request.form['s_name']
        s_sex = request.form['s_sex']
        # print(s_sex)
        g_name = request.form['g_name']
        name = Student.query.filter(Student.s_name == s_name).first()
        if name:
            msg = '学生已经存在'
            return render_template('addstu.html',msg=msg, grades=grades)
        elif s_name == '':
            msg = '添加失败,学生名为空'
            return render_template('addstu.html',msg=msg, grades=grades)
        else:
            student = Student(s_name=s_name, s_sex=s_sex, grade_id=g_name)
            db.session.add(student)
            db.session.commit()
            return redirect('/user/student/')
