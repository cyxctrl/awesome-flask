#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import todo
from .. import mongo
from ..models import Todo
import bson
import datetime

@todo.route('/todos')
def todos():
    if session.get('logged_in'):
        username = session.get('user')
        todos_id = mongo.db.user.find_one({'username':username})['todos_id']
        todo_list = []
        for tid in todos_id:
            td = mongo.db.todo.find_one(tid)
            todo_list.append(td)
        return render_template(
            'todos.html',
            todo_list=todo_list[::-1]
        )
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/todos/add',methods=['POST'])
def todo_add():
    if session.get('logged_in'):
        username = session.get('user')
        todo = Todo(
            content     = request.form.get('content'),
            create_time = datetime.datetime.utcnow()
        )
        todo.save(username)
        return redirect(url_for('.todos'))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/todos/undo/<string:todo_id>')
def todo_undo(todo_id):
    if session.get('logged_in'):
        mongo.db.todo.update(
            {'_id':bson.ObjectId(todo_id)},
            {'$set':
                {'status':1}
            }
        )
        return redirect(url_for('.todos'))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/todos/done/<string:todo_id>')
def todo_done(todo_id):
    if session.get('logged_in'):
        mongo.db.todo.update(
            {'_id':bson.ObjectId(todo_id)},
            {'$set':{'status':0}}
        )
        return redirect(url_for('.todos'))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/todos/delete/<string:todo_id>')
def todo_delete(todo_id):
    if session.get('logged_in'):
        username = session.get('user')
        mongo.db.todo.remove({'_id':bson.ObjectId(todo_id)})
        mongo.db.user.update(
            {'username':username},
            {'$pull':
                {'todos_id':bson.ObjectId(todo_id)}
            }
        )
        return redirect(url_for('.todos'))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))
