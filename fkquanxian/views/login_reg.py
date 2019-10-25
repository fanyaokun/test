from flask import Blueprint,render_template,request,jsonify,session,redirect

from models.models import db
from models.models import User
from utils.decorator import is_login

login = Blueprint('login', __name__)

# 登录
@login.route('/login', methods=['post', 'get'])
def _login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username==username, User.password==password).first()
        if user:
            session['user'] = username
            return redirect('/user/index')
        elif username == '':
            msg = '用户名不能为空'
            return render_template('login.html', msg=msg)
        elif password == '':
            msg = '密码不能为空'
            return render_template('login.html', msg=msg)
        else:
            msg = '用户名或者密码错误'
            return render_template('login.html', msg=msg)

    return render_template('login.html')

# 注册
@login.route('/reg', methods=['post','get'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['pwd1']
        password2 = request.form['pwd2']
        user = User.query.filter(User.username==username).first()
        if user:
            msg = '用户名已经存在'
            return render_template('register.html', msg=msg)
        elif password1 != password2:
            msg = '两次密码输入不一致'
            return render_template('register.html', msg=msg)
        elif username == '':
            msg = '用户名不能为空'
            return render_template('register.html', msg=msg)
        elif password1 == '':
            msg = '密码不能为空'
            return render_template('register.html', msg=msg)
        else:
            msg = '注册成功'
            user_obj = User(username=username,password=password1,role_id=2)
            db.session.add(user_obj)
            db.session.commit()
            return render_template('register.html', msg=msg)

    return render_template('register.html')

# 首页
@login.route('/index')
@is_login
def index():
    return render_template('index.html')

# 退出登录
@login.route('/logout/')
@is_login
def logout():
    del session['user']
    return redirect('/user/login')

# 头导航栏
@login.route('/head/')
@is_login
def head():
    user = session['user']
    return render_template('head.html', user=user)

# 左导航栏
@login.route('/left/')
@is_login
def left():
    user = session['user']
    permissions = User.query.filter(User.username==user).first().role.permission
    return render_template('left.html', permissions=permissions)

