#-*- coding: utf-8 -*-
from flask import Flask
from flask.ext.pymongo import PyMongo
from config import config
from .momentjs import momentjs
from flask_pagedown import PageDown
from flask.ext.login import LoginManager

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

mongo = PyMongo()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录后再操作。'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.jinja_env.globals['momentjs'] = momentjs

    mongo.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)


    from .home import home as main_blueprint
    from .auth import auth as auth_blueprint
    from .profile import profile as profile_blueprint
    from .blog import blog as blog_blueprint
    from .todo import todo as todo_blueprint
    from .markdown_page import markdown_page as markdown_page_blueprint
    from .admin_manage import admin_manage as admin_manage_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(todo_blueprint)
    app.register_blueprint(markdown_page_blueprint)
    app.register_blueprint(admin_manage_blueprint)

    return app
