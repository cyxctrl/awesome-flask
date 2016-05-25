#-*- coding: utf-8 -*-
from flask import request, render_template, flash, redirect, session, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from .. import mongo
from ..models import User, CurrentUser
from ..forms import LoginForm, RegisterForm
from ..methods import BackgroundColor, MakePoem
from flask.ext.login import login_user, logout_user
import datetime

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        if mongo.db.user.find_one({'email':form.email.data}):
            flash('邮箱已被注册。')
            return redirect(url_for('auth.register'))
        if mongo.db.user.find_one({'username':form.username.data}):
            flash('用户名已被使用。')
            return redirect(url_for('auth.register'))
        user = User(
            email           = form.email.data,
            username        = form.username.data,
            password        = generate_password_hash(form.password.data),
            register_time   = datetime.datetime.utcnow(),
            last_login_time = datetime.datetime.utcnow()
        )
        user.save()
        if user.username == 'admin':
            mongo.db.user.update(
                {'username':user.username},
                {'$set':{'permission':9}}
                )
        flash('注册成功！')
        return redirect(url_for('auth.login'))
    backgroundColor = BackgroundColor()
    text = MakePoem()
    return render_template('auth/register.html',form=form,backgroundColor=backgroundColor,text=text)

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username_login = form.username.data
        password_login = form.password.data
        if '@' in username_login:
            user = mongo.db.user.find_one({'email':username_login})
        else:
            user = mongo.db.user.find_one({'username':username_login})
        if user is not None and check_password_hash(user['password'],password_login):
            user_obj = CurrentUser(
                username    = user['username'],
                email       = user['email'],
                permission  = user['permission'],
                blogs_id    = user['blogs_id'],
                todos_id    = user['todos_id'],
                markdown_id = user['markdown_id'],
                following   = user['following']
                )
            mongo.db.user.update(
                {'username':user_obj.username},
                {'$set':{'last_login_time':datetime.datetime.utcnow()}}
            )
            login_user(user_obj,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('profile.user',username=user['username']))
        flash('错误或不存在的邮箱、用户名和密码。')
    backgroundColor = BackgroundColor()
    text = MakePoem()
    return render_template('auth/login.html',form=form,backgroundColor=backgroundColor,text=text)

@auth.route('/logout')
def logout():
    logout_user()
    backgroundColor = BackgroundColor()
    text = MakePoem()
    flash('注销成功！')
    return render_template('home/index.html',backgroundColor=backgroundColor,text=text)


