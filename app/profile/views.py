#-*- coding: utf-8 -*-
from flask import render_template, redirect, session, url_for, abort, request
from . import profile
from .. import mongo
from flask.ext.login import login_required, current_user


@profile.route('/<username>')
@login_required
def user(username):
    user = mongo.db.user.find_one({'username':username})
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

@profile.route('/modify_password')
def modify_password():
    pass

@profile.route('/modify_email')
def modify_email():
    pass

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

