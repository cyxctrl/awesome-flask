#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import todo
from .. import mongo
from ..models import Todo
import bson
import datetime
from flask.ext.login import login_required, current_user

@todo.route('/todos')
@login_required
def todos():
    username = current_user.username
    todos_id = mongo.db.user.find_one({'username':username})['todos_id']
    todo_list = []
    for tid in todos_id:
        td = mongo.db.todo.find_one(tid)
        todo_list.append(td)
    return render_template(
        'todos.html',
        todo_list=todo_list[::-1]
    )

@todo.route('/todos/add',methods=['POST'])
@login_required
def todo_add():
    username = current_user.username
    todo = Todo(
        content     = request.form.get('content'),
        create_time = datetime.datetime.utcnow()
    )
    todo.save(username)
    return redirect(url_for('.todos'))

@todo.route('/todos/undo/<string:todo_id>')
@login_required
def todo_undo(todo_id):
    mongo.db.todo.update(
        {'_id':bson.ObjectId(todo_id)},
        {'$set':
            {'status':1}
        }
    )
    return redirect(url_for('.todos'))

@todo.route('/todos/done/<string:todo_id>')
@login_required
def todo_done(todo_id):
    mongo.db.todo.update(
        {'_id':bson.ObjectId(todo_id)},
        {'$set':{'status':0}}
    )
    return redirect(url_for('.todos'))

@todo.route('/todos/delete/<string:todo_id>')
@login_required
def todo_delete(todo_id):
    username = current_user.username
    mongo.db.todo.remove({'_id':bson.ObjectId(todo_id)})
    mongo.db.user.update(
        {'username':username},
        {'$pull':
            {'todos_id':bson.ObjectId(todo_id)}
        }
    )
    return redirect(url_for('.todos'))

