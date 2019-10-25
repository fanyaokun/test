from flask import Blueprint,render_template,request,jsonify,session,redirect
from sqlalchemy import false

from models.models import Grade,Student
from utils.decorator import is_login
from models.models import db

classroom = Blueprint('classroom', __name__)

# 班级管理
@classroom.route('/grade/')
@is_login
def grade():
    # grades = Grade.query.all()
    page = int(request.args.get('page', 1))
    paginate = Grade.query.paginate(page, 2, error_out=false)
    return render_template('grade.html', paginate=paginate)

# 删除班级
@classroom.route('/deleteclass/<id>')
@is_login
def delete(id):
    grade = Grade.query.filter(Grade.g_id == id).first()
    db.session.delete(grade)
    db.session.commit()
    return redirect('/user/grade/')

# 添加班级
@classroom.route('/addgrade/', methods=['post','get'])
@is_login
def addgrade():
    if request.method == 'POST':
        g_name = request.form['g_name']
        name = Grade.query.filter(Grade.g_name == g_name).first()
        if name:
            msg = '班级已经存在'
            return render_template('addgrade.html',msg=msg)
        elif g_name == '':
            msg = '添加失败,班级为空'
            return render_template('addgrade.html',msg=msg)
        else:
            classroom = Grade(g_name=g_name)
            db.session.add(classroom)
            db.session.commit()
            return redirect('/user/grade/')

    return render_template('addgrade.html')

# 编辑班级
@classroom.route('/edit_grade/<id>', methods=['post','get'])
@is_login
def edit_grade(id):
    grade = Grade.query.filter(Grade.g_id == id).first()
    if request.method == 'GET':
        return render_template('edit_grade.html', grade=grade, time=grade.g_create_time)
    if request.method == 'POST':
        classroom = request.form['g_name']
        creat_time = request.form['g_creat_time']
        grade_obj = Grade.query.filter(Grade.g_name == classroom).first()
        if grade_obj:
            grade.g_create_time = creat_time
            db.session.commit()
            msg = f'{classroom}班级已经存在'
            msg1 = f'创建时间修改成功'
            return render_template('edit_grade.html', grade=grade, msg=msg, msg1=msg1, time=grade.g_create_time)
        elif classroom == '':
            msg = '班级名称不能为空'
            return render_template('edit_grade.html', grade=grade, msg=msg, time=grade.g_create_time)
        else:
            grade.g_name = classroom
            grade.g_create_time = creat_time
            db.session.commit()
            return redirect('/user/grade/')

# 查看学生
@classroom.route("/grade_student/<id>/", methods=['post','get'])
@is_login
def grade_student(id):
    grade = Grade.query.filter(Grade.g_id == id).first()
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        paginate = Student.query.filter(Student.grade_id == id).paginate(page, 2, error_out=false)
        return render_template('grade_student.html', grade=grade, paginate=paginate)

