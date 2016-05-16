#-*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for, abort, request, flash
from . import profile
from .. import mongo
from ..forms import EditProfileForm, ValidatePasswordForm, EditPasswordForm, EditPasswordQuestionsForm, ValidateUserForm, ValidatePasswordQuestionsForm
from flask.ext.login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@profile.route('/<username>')
def user(username):
    user = mongo.db.user.find_one({'username':username})
    if user is None:
        abort(404)
    elif current_user.is_authenticated and current_user.username == username:
        return render_template('profile/current_user.html',user=user)
    else:
        blog_list = []
        for bid in user['blogs_id']:
            bg = mongo.db.blog.find_one(bid)
            if bg['permission'] == 'public':
                blog_list.append(bg)
        blog_list = sorted(blog_list,key=lambda e:e['last_modify_time'],reverse=True)
        return render_template('profile/user.html',user=user,blog_list=blog_list)

@profile.route('/follow/<username>')
@login_required
def follow(username):
    c_username = current_user.username
    f_username = username
    mongo.db.user.update(
        {'username':c_username},
        {'$push':
            {'following':f_username}
        }
    )
    return redirect(url_for('profile.user',username=f_username))

@profile.route('/unfollow/<username>')
@login_required
def unfollow(username):
    c_username = current_user.username
    f_username = username
    aim = request.headers.get('Referer')
    mongo.db.user.update(
        {'username':c_username},
        {'$pull':
            {'following':f_username}
        }
    )
    return redirect(aim)

@profile.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        mongo.db.user.update(
            {'username':current_user.username},
            {'$set':
                {
                    'location':form.location.data,
                    'about_me':form.about_me.data
                }
            }
        )
        flash('你的个人信息已更新。')
        return redirect(url_for('.user', username=current_user.username))
    user = mongo.db.user.find_one({'username':current_user.username})
    form.email.data = user['email']
    form.username.data = user['username']
    form.location.data = user['location']
    form.about_me.data = user['about_me']
    return render_template('profile/edit_profile.html', form=form)

@profile.route('/validate-password-ep',methods=['GET','POST'])
@login_required
def validate_password_edit_password():
    form = ValidatePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = mongo.db.user.find_one({'username':current_user.username})
        if check_password_hash(user['password'],form.password.data):
            session['edit_password'] = True
            action = url_for('profile.edit_password')
            return redirect(url_for('.edit_password',action=action))
        else:
            flash('密码验证不通过！')
    action = url_for('profile.validate_password_edit_password')
    tips = '需要验证旧密码才能修改密码。'
    return render_template('profile/validate_password.html',form=form,action=action,tips=tips)

@profile.route('/edit-password', methods=['GET', 'POST'])
@login_required
def edit_password():
    if session.get('edit_password'):
        form = EditPasswordForm()
        if request.method == 'POST' and form.validate_on_submit():
            mongo.db.user.update(
                {'username':current_user.username},
                {'$set':
                    {'password':generate_password_hash(form.password.data)}
                }
            )
            session.pop('edit_password',None)
            flash('密码修改成功！')
            return redirect(url_for('profile.user',username=current_user.username))
        return render_template('profile/edit_password.html',form=form)
    else:
        abort(404)

@profile.route('/validate-password-epq',methods=['GET','POST'])
@login_required
def validate_password_edit_password_questions():
    form = ValidatePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = mongo.db.user.find_one({'username':current_user.username})
        if check_password_hash(user['password'],form.password.data):
            session['edit_password_questions'] = True
            action = url_for('profile.edit_password_questions')
            return redirect(url_for('.edit_password_questions',action=action))
        else:
            flash('无法通过密码验证！')
    action = url_for('profile.validate_password_edit_password_questions')
    tips = '需要验证密码才能修改密保。'
    return render_template('profile/validate_password.html',form=form,action=action,tips=tips)

@profile.route('/edit-password-questions', methods=['GET', 'POST'])
@login_required
def edit_password_questions():
    if session.get('edit_password_questions'):
        form = EditPasswordQuestionsForm()
        if request.method == 'POST' and form.validate_on_submit():
            question1 = form.question1.data
            answer1 = form.answer1.data
            question2 = form.question2.data
            answer2 = form.answer2.data
            mongo.db.user.update(
                {'username':current_user.username},
                {'$set':
                    {'password_questions':
                        [
                            question1,answer1,question2,answer2
                        ]
                    }
                }
            )
            session.pop('edit_password_questions',None)
            flash('密保问题修改成功！')
            return redirect(url_for('profile.user',username=current_user.username))
        user = mongo.db.user.find_one({'username':current_user.username})
        if user['password_questions']:
            form.question1.data = user['password_questions'][0]
            form.answer1.data = user['password_questions'][1]
            form.question2.data = user['password_questions'][2]
            form.answer2.data = user['password_questions'][3]
        return render_template('profile/edit_password_questions.html', form=form)
    else:
        abort(404)

@profile.route('/validate-password-du',methods=['GET','POST'])
@login_required
def validate_password_delete_user():
    form = ValidatePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = mongo.db.user.find_one({'username':current_user.username})
        if check_password_hash(user['password'],form.password.data):
            session['delete_user'] = True
            return redirect(url_for('.delete_user'))
        else:
            flash('无法通过密码验证！')
    action = url_for('profile.validate_password_delete_user')
    tips = '需要验证密码才能删除账户。'
    return render_template('profile/validate_password.html',form=form,action=action,tips=tips)

@profile.route('/delete-user')
@login_required
def delete_user():
    if session.get('delete_user'):
        username = current_user.username
        blogs_id = mongo.db.user.find_one({'username':username})['blogs_id']
        for bid in blogs_id:
            mongo.db.blog.find_one_and_delete({'_id':bid})
        todos_id = mongo.db.user.find_one({'username':username})['todos_id']
        for tid in todos_id:
            mongo.db.todo.find_one_and_delete({'_id':tid})
        markdown_id = mongo.db.user.find_one({'username':username})['markdown_id']
        mongo.db.markdown.find_one_and_delete({'_id':markdown_id})
        mongo.db.user.remove({'username':username})
        session.pop('delete_user',None)
        flash('账户删除成功！')
        return redirect(url_for('home.index'))
    else:
        abort(404)

@profile.route('/validate-user',methods=['GET','POST'])
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
    return render_template('profile/validate_user.html',form=form)

@profile.route('/validate-password-questions',methods=['GET','POST'])
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
                return redirect(url_for('.set_password'))
            else:
                flash('无法通过密保问题验证！')
        form.email.data = session.get('forget_email')
        form.username.data = session.get('forget_username')
        return render_template(
            'profile/validate_password_questions.html',form=form,question1=question1,question2=question2)

@profile.route('/set-password',methods=['GET','POST'])
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
        action = url_for('profile.set_password')
        return render_template('profile/edit_password.html',action=action,form=form)
    else:
        abort(404)