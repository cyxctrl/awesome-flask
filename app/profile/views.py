#-*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for, abort, request, flash
from . import profile
from .. import mongo
from ..forms import EditProfileForm, EditPasswordForm, EditPasswordQuestionForm
from flask.ext.login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@profile.route('/<username>')
@login_required
def user(username):
    user = mongo.db.user.find_one({'username':username})
    if user is None:
        abort(404)
    blog_list = []
    for bid in user['blogs_id']:
        bg = mongo.db.blog.find_one(bid)
        blog_list.append(bg)
    return render_template('user.html',user=user,blog_list=blog_list)

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
        flash(u'你的个人信息已更新。')
        return redirect(url_for('.user', username=current_user.username))
    user = mongo.db.user.find_one({'username':current_user.username})
    form.email.data = user['email']
    form.username.data = user['username']
    form.location.data = user['location']
    form.about_me.data = user['about_me']
    return render_template('edit_profile.html', form=form)

@profile.route('/edit-password', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = EditPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = mongo.db.user.find_one({'username':current_user.username})
        if check_password_hash(user['password'],form.old_password.data):
            mongo.db.user.update(
                {'username':current_user.username},
                {'$set':
                    {'password':generate_password_hash(form.new_password.data)}
                }
            )
            flash('密码修改成功！')
            return redirect(url_for('profile.user',username=current_user.username))
        else:
            flash('旧密码不正确！')
    return render_template("edit_password.html", form=form)

@profile.route('/edit-password-question', methods=['GET', 'POST'])
@login_required
def edit_password_question():
    form = EditPasswordQuestionForm()
    user = mongo.db.user.find_one({'username':current_user.username})
    if request.method == 'POST' and form.validate_on_submit():
        if check_password_hash(user['password'],form.password.data):
            question1 = form.question1.data
            answer1 = form.answer1.data
            question2 = form.question2.data
            answer2 = form.answer2.data
            mongo.db.user.update(
                {'username':current_user.username},
                {'$set':
                    {'password_questions':
                        [
                            {question1:answer1},
                            {question2:answer2}
                        ]
                    }
                }
            )
            flash('密保问题修改成功！')
            return redirect(url_for('profile.user',username=current_user.username))
        else:
            flash('密码验证不通过！')
    for (q,a) in user['password_questions'][0].items():
        form.question1.data = q
        form.answer1.data = a
    for (q,a) in user['password_questions'][1].items():
        form.question2.data = q
        form.answer2.data = a
    return render_template('edit_password_question.html', form=form)
