#-*- coding: utf-8 -*-
from flask import request, render_template, flash, redirect, session, url_for
from . import auth
from .. import mongo
from ..models import User

@auth.route('/register',methods=['POST','GET'])
def register():
    username_register = request.form['username']
    password_register = request.form['password']
    if request.method == 'POST':
        if mongo.db.user.find_one({'username':username_register}):
            flash('用户名已存在！')
            return redirect(url_for('main.index'))
        user = User(username=username_register,password=password_register)
        user.save()
        flash('注册成功！')
        return redirect(url_for('main.index'))
    flash('出错了？')
    return render_template('index.html')

@auth.route('/login',methods=['POST','GET'])
def login():
    username_login = request.form['username']
    password_login = request.form['password']
    if request.method == 'POST':
        if mongo.db.user.find_one({'username':username_login,'password':password_login}):
            session['logged_in'] = True
            session['user'] = username_login
            return redirect(url_for('main.index'))
    flash('用户不存在？账号错误？密码错误？')
    return render_template('index.html')

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('注销成功！')
    return redirect(url_for('main.index'))