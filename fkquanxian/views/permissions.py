from flask import Blueprint,render_template,request,jsonify,session,redirect
from sqlalchemy import false

from models.models import Permission
from utils.decorator import is_login
from models.models import db

permissions = Blueprint('permissions', __name__)

# 权限管理
@permissions.route('/permissions/')
@is_login
def _permissions():
    permissions = Permission.query.all()
    return render_template('permissions.html', permissions=permissions)

# 删除权限
@permissions.route('/deleteper/<id>')
@is_login
def delete(id):
    permission = Permission.query.filter(Permission.p_id == id).first()
    db.session.delete(permission)
    db.session.commit()
    return redirect('/user/permissions/')

# 添加权限
@permissions.route('/addpermission/', methods=['post','get'])
@is_login
def addpermission():
    if request.method == 'GET':
        pers = Permission.query.all()
        return render_template('addpermission.html', pers=pers)
    if request.method == 'POST':
        pers = Permission.query.all()
        p_name = request.form['p_name']
        p_er = request.form['p_er']
        name1 = Permission.query.filter(Permission.p_name == p_name).first()
        name2 = Permission.query.filter(Permission.p_er == p_er).first()
        if name1:
            msg = '权限名已经存在'
            return render_template('addpermission.html', msg=msg, pers=pers)
        elif name2:
            msg1 = '权限简写已经存在'
            return render_template('addpermission.html', msg1=msg1, pers=pers)
        elif p_name == '':
            msg = '添加失败,权限名为空'
            return render_template('addpermission.html', msg=msg, pers=pers)
        elif p_er == '':
            msg1 = '添加失败,权限简写为空'
            return render_template('addpermission.html', msg1=msg1, pers=pers)
        else:
            permission = Permission(p_name=p_name, p_er=p_er)
            db.session.add(permission)
            db.session.commit()
            return redirect('/user/permissions/')

# 编辑权限
@permissions.route('/eidtorpermission/<id>', methods=['post','get'])
@is_login
def eidtorpermission(id):
    permission = Permission.query.filter(Permission.p_id == id).first()
    if request.method == 'GET':
        return render_template('eidtorpermission.html', permission=permission)
    if request.method == 'POST':
        p_name = request.form['p_name']
        p_er = request.form['p_er']
        # print(p_name, p_er)
        per_obj1 = Permission.query.filter(Permission.p_name == p_name).first()
        per_obj2 = Permission.query.filter(Permission.p_er == p_er).first()
        if per_obj1:
            msg = '权限名已经存在'
            return render_template('eidtorpermission.html', permission=permission, msg=msg)
        elif per_obj2:
            msg = '权限简写已经存在'
            return render_template('eidtorpermission.html', permission=permission, msg1=msg)
        elif p_name == '':
            msg = '权限名不能为空'
            return render_template('eidtorpermission.html', permission=permission, msg=msg)
        elif p_er == '':
            msg1 = '权限简写不能为空'
            return render_template('eidtorpermission.html', permission=permission, msg1=msg1)
        else:
            permission.p_name = p_name
            permission.p_er = p_er
            db.session.commit()
            return redirect('/user/permissions/')


