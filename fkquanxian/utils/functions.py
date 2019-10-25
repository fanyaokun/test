import os


from flask import Flask

from views.login_reg import login
from views.classroom import classroom
from views.student import student
from views.role import role
from views.permissions import permissions
from views.user import user

from models.models import db


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.register_blueprint(blueprint=login, url_prefix='/user')
    app.register_blueprint(blueprint=classroom, url_prefix='/user')
    app.register_blueprint(blueprint=student, url_prefix='/user')
    app.register_blueprint(blueprint=role, url_prefix='/user')
    app.register_blueprint(blueprint=permissions, url_prefix='/user')
    app.register_blueprint(blueprint=user, url_prefix='/user')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/fkquanxian'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app=app)

    with app.app_context():
        db.create_all()

    return app
