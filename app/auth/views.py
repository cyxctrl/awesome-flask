#-*- coding: utf-8 -*-
from flask import request, render_template, flash, redirect, session, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from .. import mongo
from ..models import User, CurrentUser
from ..forms import LoginForm, RegisterForm, ValidateUserForm, ValidatePasswordQuestionsForm, EditPasswordForm
import datetime
from flask.ext.login import login_user, logout_user

text = 'Life is short, and you need Python.'

def backgroundPicture(timestamp):
    name = int(timestamp % 10)
    bgname = str(name) + '.jpg'
    return bgname

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
    bgname = backgroundPicture(datetime.datetime.utcnow().timestamp())
    return render_template('auth/register.html',form=form,bgname=bgname,text=text)

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
    bgname = backgroundPicture(datetime.datetime.utcnow().timestamp())
    return render_template('auth/login.html',form=form,bgname=bgname,text=text)

@auth.route('/logout')
def logout():
    logout_user()
    flash('注销成功！')
    bgname = backgroundPicture(datetime.datetime.utcnow().timestamp())
    return render_template('home/index.html',bgname=bgname,text=text)

@auth.route('/validate-user',methods=['GET','POST'])
def validate_user():
    form = ValidateUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        user = mongo.db.user.find_one({'email':email,'username':username})
        if user is not None:
            session['forget_email'] = email
            session['forget_username'] = username
            return redirect(url_for('.validate_password_questions'))
        else:
            flash('没有这个用户！')
    return render_template('auth/validate_user.html',form=form)

@auth.route('/validate-password-questions',methods=['GET','POST'])
def validate_password_questions():
    if session.get('forget_email') is None or session.get('forget_username') is None:
        abort(404)
    else:
        form = ValidatePasswordQuestionsForm()
        email = session.get('forget_email')
        username = session.get('forget_username')
        user = mongo.db.user.find_one({'email':email,'username':username})
        if user is None:
            flash('没有这个用户！')
            return redirect('.validate_user')
        if user['password_questions']:
            question1 = user['password_questions'][0]
            question2 = user['password_questions'][2]
        else:
            flash('你还没有设置密保问题，请联系管理员进行密码找回！')
            return redirect(url_for('auth.login'))
        if request.method == 'POST' and form.validate_on_submit():
            answer1 = user['password_questions'][1]
            answer2 = user['password_questions'][3]
            if form.answer1.data == answer1 and form.answer2.data == answer2:
                session['set_password'] = True
                return redirect(url_for('auth.set_password'))
            else:
                flash('无法通过密保问题验证！')
        form.email.data = session.get('forget_email')
        form.username.data = session.get('forget_username')
        return render_template(
            'auth/validate_password_questions.html',form=form,question1=question1,question2=question2)

@auth.route('/set-password',methods=['GET','POST'])
def set_password():
    form = EditPasswordForm()
    if session.get('forget_email') and session.get('forget_username') and session.get('set_password'):
        username = session.get('forget_username')
        email = session.get('forget_email')
        if mongo.db.user.find_one({'username':username,'email':email}) is None:
            flash('没有这个用户！')
            return redirect('.validate_user')
        if request.method == 'POST' and form.validate_on_submit():
            mongo.db.user.update(
                {'username':username,'email':email},
                {'$set':
                    {'password':generate_password_hash(form.password.data)}
                }
            )
            session.pop('forget_email',None)
            session.pop('forget_username',None)
            session.pop('set_password',None)
            flash('您已设置新密码！！')
            return redirect(url_for('auth.login'))
        action = url_for('auth.set_password')
        return render_template('profile/edit_password.html',action=action,form=form)
    else:
        abort(404)
