#-*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, session, flash
from . import home
from ..forms import PageDownForm
import random
from flask.ext.login import current_user

@home.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@home.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@home.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile.user',username=current_user.username))
    bgname = str(int(random.random()*20))+'.jpg'
    return render_template('index.html',bgname=bgname)
