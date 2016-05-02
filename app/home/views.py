#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import home
import random

@home.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@home.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@home.route('/test')
def test():
    return render_template('editor.html')

@home.route('/')
def index():
    if session.get('logged_in'):
        username = session.get('user')
        return redirect(url_for('profile.user',username=username))
    bgname = str(int(random.random()*20))+'.jpg'
    return render_template('index.html',bgname=bgname)




