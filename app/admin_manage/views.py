#-*- coding: utf-8 -*-
from flask import request, render_template, flash, redirect, session, url_for, abort
from werkzeug.security import generate_password_hash
from . import admin_manage
from .. import mongo
from ..forms import AdminManageProfileForm
import datetime
from flask.ext.login import login_user, logout_user, login_required, current_user

@admin_manage.route('/admin-manage/<username>/profile',methods=['GET','POST'])
@login_required
def admin_manage_profile(username):
    if current_user.permission == 9:
        user = mongo.db.user.find_one({'username':username})
        if user is None:
            return abort(404)
        form = AdminManageProfileForm()
        if request.method == 'POST' and form.validate_on_submit():
            new_username = form.username.data
            email = form.email.data
            question1 = form.question1.data
            answer1 = form.answer1.data
            question2 = form.question2.data
            answer2= form.answer2.data
            permission = int(form.permission.data)
            register_time = datetime.datetime.strptime(form.register_time.data,'%Y-%m-%d %H:%M:%S')
            following = form.following.data.split(',')
            location = form.location.data
            about_me = form.about_me.data
            mongo.db.user.update(
                {'username':username},
                {'$set':
                    {
                        'username':new_username,
                        'email':email,
                        'password_questions':[question1,answer1,question2,question2],
                        'permission':permission,
                        'register_time':register_time,
                        'following':following,
                        'location':location,
                        'about_me':about_me
                    }
                }
            )
            flash('信息更新成功！')
            return redirect(url_for('admin_manage.admin_manage_profile',username=new_username))
        form.username.data = user['username']
        form.email.data = user['email']
        if user['password_questions']:
            form.question1.data = user['password_questions'][0]
            form.answer1.data = user['password_questions'][1]
            form.question2.data = user['password_questions'][2]
            form.answer2.data = user['password_questions'][3]
        form.permission.data = user['permission']
        form.register_time.data = user['register_time'].strftime('%Y-%m-%d %H:%M:%S')
        form.following.data = ','.join(user['following'])
        form.location.data = user['location']
        form.about_me.data = user['about_me']
        session['delete_user'] = True
        return render_template('admin_manage/admin_manage_profile.html',form=form,username=user['username'])
    else:
        abort(404)

@admin_manage.route('/admin-manage/<username>/delete-user')
@login_required
def delete_user(username):
    if session.get('delete_user'):
        mongo.db.user.remove({'username':username})
        session.pop('delete_user',None)
        flash(u'账户删除成功！')
        return redirect(url_for('home.index'))
    else:
        abort(404)

