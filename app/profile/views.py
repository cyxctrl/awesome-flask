#-*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for
from . import profile
from .. import mongo

@profile.route('/<username>')
def user(username):
    if username == session.get('user') and session.get('logged_in'):
        user = mongo.db.user.find_one({'username':username})
        return render_template('user.html',user=user)
    else:
        return redirect(url_for('main.index'))