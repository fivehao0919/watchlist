import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')    # 等同于 app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数, 接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象

login_manager.login_view = 'login'

@app.context_processor
def inject_user():  # 函数名可以随意修改
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)  # 需要返回字典, 等同于return {'user': user}

from watchlist import views, errors, commands