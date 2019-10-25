from flask import Blueprint,render_template,request,jsonify,session,redirect
from sqlalchemy import false

from models.models import User,Role
from utils.decorator import is_login
from models.models import db

user = Blueprint('user', __name__)

# 用户列表
@user.route('/userlist/')
@is_login
def _user():
    page = int(request.args.get('page', 1))
    paginate = User.query.paginate(page, 2, error_out=false)
    return render_template('users.html', paginate=paginate)

# 删除用户
@user.route('/deleteuser/<id>')
@is_login
def delete(id):
    user = User.query.filter(User.u_id == id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/user/userlist/')

# 添加用户
@user.route('/adduser/', methods=['post','get'])
@is_login
def adduser():
    if request.method == 'GET':
        users = User.query.all()
        return render_template('adduser.html', users=users)
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        user = User.query.filter(User.username == username).first()
        if user:
            msg = '用户名已经存在'
            return render_template('adduser.html', msg=msg)
        elif password1 != password2:
            msg = '两次密码输入不一致'
            return render_template('adduser.html', msg=msg)
        elif username == '':
            msg = '添加失败,角色名为空'
            return render_template('adduser.html', msg=msg)
        else:
            user = User(username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect('/user/userlist/')

# 修改密码
@user.route('/changepwd/', methods=['post','get'])
@is_login
def changepwd():
    if request.method == 'GET':
        username = session.get('user')
        user = User.query.filter(User.username == username).first()
        return render_template('changepwd.html', user=user)
    if request.method == 'POST':
        username = session.get('user')
        password1 = request.form['pwd1']
        password2 = request.form['pwd2']
        password3 = request.form['pwd3']
        user = User.query.filter(User.username == username).first()
        if user.password != password1:
            msg = '旧密码输入错误'
            return render_template('changepwd.html', user=user, msg=msg)
        elif password2 != password3:
            msg = '两次密码输入不一致'
            return render_template('changepwd.html', user=user, msg=msg)
        else:
            user.password = password2
            db.session.commit()
            msg = '密码修改成功'
            return render_template('changepwdsu.html', msg=msg)

# 分配角色
@user.route('/assignrole/<id>', methods=['post','get'])
@is_login
def assignrole(id):
    user = User.query.filter(User.u_id == id).first()
    roles = Role.query.all()
    if request.method == 'GET':
        return render_template('assign_user_role.html', roles=roles, user=user)
    if request.method == 'POST':
        r_id = request.form['r_id']
        user.role_id = r_id
        db.session.commit()
        return redirect('/user/userlist/')
