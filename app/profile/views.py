#-*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for, g
from . import profile
from .. import mongo
from flask.ext.login import login_required, current_user

@profile.before_request
def before_request():
    g.user = current_user

@profile.route('/user/<username>')
@login_required
def user(username):
    return render_template('user.html')

@profile.route('/modify_password')
def modify_password():
    pass

@profile.route('/modify_email')
def modify_email():
    pass

