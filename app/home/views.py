#-*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, session, flash
from . import home
from ..forms import PageDownForm
from flask.ext.login import current_user
from ..auth.views import backgroundPicture, text
import datetime

@home.app_errorhandler(404)
def page_not_found(e):
    return render_template('home/404.html'), 404

@home.app_errorhandler(500)
def internal_server_error(e):
    return render_template('home/500.html'), 500

@home.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile.user',username=current_user.username))
    bgname = backgroundPicture(datetime.datetime.utcnow().timestamp())
    return render_template('home/index.html',bgname=bgname,text=text)
