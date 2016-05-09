#-*- coding: utf-8 -*-
from flask import Flask
from flask.ext.pymongo import PyMongo
from config import config
from .momentjs import momentjs
from flask_pagedown import PageDown
from flask.ext.login import LoginManager

mongo = PyMongo()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u'请登陆后再操作。'
login_manager.remember_cookie_name = u'remember_me_token'

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
    from .markdownpage import markdownpage as markdownpage_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(todo_blueprint)
    app.register_blueprint(markdownpage_blueprint)

    return app

#db = pymongo.MongoClient('localhost', 27017).awesome_flask
#db = pymongo.MongoClient("mongo.duapp.com", 8908).oLNwgqNbtTNsiNjFoDGn
