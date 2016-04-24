#-*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for
from . import profile

@profile.route('/<username>')
def user(username):
    if username == session.get('user') and session.get('logged_in'):
        return render_template('user.html')
    else:
        return redirect(url_for('main.index'))