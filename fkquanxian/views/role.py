from flask import Blueprint,render_template,request,jsonify,session,redirect
from sqlalchemy import false

from models.models import Role,Permission,r_p
from utils.decorator import is_login
from models.models import db

role = Blueprint('role', __name__)

# 角色列表
@role.route('/roles/')
@is_login
def _role():
    roles = Role.query.all()
    return render_template('roles.html', roles=roles)

# 添加角色
@role.route('/addroles/', methods=['post','get'])
@is_login
def addroles():
    if request.method == 'GET':
        roles = Role.query.all()
        return render_template('addroles.html', roles=roles)
    if request.method == 'POST':
        r_name = request.form['r_name']
        name = Role.query.filter(Role.r_name == r_name).first()
        if name:
            msg = '角色已经存在'
            return render_template('addroles.html', msg=msg)
        elif r_name == '':
            msg = '添加失败,角色名为空'
            return render_template('addroles.html', msg=msg)
        else:
            role = Role(r_name=r_name)
            db.session.add(role)
            db.session.commit()
            return redirect('/user/roles/')


# 查看角色权限
@role.route('/userperlist/<id>', methods=['post','get'])
@is_login
def userperlist(id):
    role = Role.query.filter(Role.r_id == id).first()
    if request.method == 'GET':
        permissions = role.permission
        return render_template('user_per_list.html', user=role.r_name,r_id=role.r_id, pers=permissions)

# 删除角色权限
@role.route('/deleterole_per/<id>', methods=['post','get'])
@is_login
def deleterole_per(id):
    r_id = request.form['r_id']
    if request.method == 'POST':
        role = Role.query.filter(Role.r_id == r_id).first()
        per = Permission.query.filter(Permission.p_id == id).first()
        per.roles.remove(role)
        db.session.commit()
        return redirect(f'/user/userperlist/{r_id}')

# 添加角色权限
@role.route('/adduserper/<id>', methods=['post','get'])
@is_login
def adduserper(id):
    role = Role.query.filter(Role.r_id == id).first()
    permissions = Permission.query.all()
    if request.method == 'GET':
        return render_template('add_user_per.html', permissions=permissions, role=role)
    if request.method == 'POST':
        p_id = request.form['p_id']
        per = Permission.query.filter(Permission.p_id == p_id).first()
        per.roles.append(role)
        db.session.commit()
        return redirect('/user/roles/')

