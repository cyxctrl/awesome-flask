#-*- coding: utf-8 -*-
from flask import request, render_template, flash, redirect, session, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from .. import mongo
from ..models import User
from ..forms import LoginForm, RegisterForm
import datetime
import random

@auth.route('/register',methods=['GET','POST'])
def register():
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        user = User(
            email           = registerform.email.data,
            username        = registerform.username.data,
            password        = generate_password_hash(registerform.password.data),
            register_time   = datetime.datetime.utcnow(),
            last_login_time = datetime.datetime.utcnow()
        )
        user.save()
        flash('注册成功！')
        return redirect(url_for('auth.login'))
    bgname = str(int(random.random()*20))+'.jpg'
    return render_template('register.html',registerform=registerform,bgname=bgname)

@auth.route('/login',methods=['GET','POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        username_login = loginform.username.data
        password_login = loginform.password.data
        if '@' in username_login:
            user = mongo.db.user.find_one({'email':username_login})
        else:
            user = mongo.db.user.find_one({'username':username_login})
        if user is not None and check_password_hash(user['password'],password_login):
            session['logged_in'] = True
            session['user']      = user['username']
            mongo.db.user.update(
                {'username':user['username']},
                {'$set':{'last_login_time':datetime.datetime.utcnow()}}
            )
            return redirect(url_for('profile.user',username=user['username']))
        flash('错误或不存在的邮箱、用户名和密码。')
    bgname = str(int(random.random()*20))+'.jpg'
    return render_template('login.html',loginform=loginform,bgname=bgname)

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('注销成功！')
    bgname = str(int(random.random()*20))+'.jpg'
    return render_template('index.html',bgname=bgname)