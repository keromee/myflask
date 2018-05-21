#!coding=UTF-8
import os 
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_babelex import Babel
from flask_migrate import Migrate, MigrateCommand

# Create flask app
# 打个标记
app = Flask(__name__, template_folder='templates')
app.debug = True

# Initialize babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'zh_CN')

# Flask and Flask-SQLAlchemy initialization here 支持 emoji 表情符号
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://lovecard:Moyunqiang1984@rm-2zehp93770kjy35e2o.mysql.rds.aliyuncs.com:3306/myway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Flask views
@app.route('/')
@app.route('/admin')
def index():
        tmp = u"""
        <p><a href="/admin/?lang=en">Click me to get to Admin! (English)</a></p>
        <p><a href="/admin/?lang=cs">Click me to get to Admin! (Czech)</a></p>
        <p><a href="/admin/?lang=de">Click me to get to Admin! (German)</a></p>
        <p><a href="/admin/?lang=es">Click me to get to Admin! (Spanish)</a></p>
        <p><a href="/admin/?lang=fa">Click me to get to Admin! (Farsi)</a></p>
        <p><a href="/admin/?lang=fr">Click me to get to Admin! (French)</a></p>
        <p><a href="/admin/?lang=pt">Click me to get to Admin! (Portuguese)</a></p>
        <p><a href="/admin/?lang=ru">Click me to get to Admin! (Russian)</a></p>
        <p><a href="/admin/?lang=zh_CN">Click me to get to Admin! (Chinese - Simplified)</a></p>
        <p><a href="/admin/?lang=zh_TW">Click me to get to Admin! (Chinese - Traditional)</a></p>
        """
        return tmp

