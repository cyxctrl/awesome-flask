#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import todo
from .. import mongo
from ..models import Todo
from ..forms import TodoForm
import bson
import datetime
from flask.ext.login import login_required, current_user

@todo.route('/todos',methods=['GET','POST'])
@login_required
def todos():
    form = TodoForm()
    username = current_user.username
    if request.method == 'POST' and form.validate_on_submit():
        todo = Todo(
            content = request.form.get('content'),
            create_time=datetime.datetime.utcnow())
        todo.save(username)
        return redirect(url_for('.todos'))
    todos_id = mongo.db.user.find_one({'username':username})['todos_id']
    todo_list = []
    for tid in todos_id:
        td = mongo.db.todo.find_one(tid)
        todo_list.append(td)
    action = url_for('todo.todos')
    return render_template('todo/todos.html',form=form,todo_list=todo_list[::-1],action=action)

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
    flash('待办事项删除成功！')
    return redirect(url_for('.todos'))

