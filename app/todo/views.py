#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import todo
from .. import mongo
from ..models import Todo
import bson
import datetime

@todo.route('/<username>/todos')
def todos(username):
    if username == session.get('user') and session.get('logged_in'):
        todos_id = mongo.db.user.find_one({'username':username})['todos_id']
        todo_list = []
        for tid in todos_id:
            td = mongo.db.todo.find_one(tid)
            todo_list.append(td)
        return render_template('todos.html',todo_list=todo_list[::-1])
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/<username>/todos/add',methods=['POST',])
def todo_add(username):
    if username == session.get('user') and session.get('logged_in'):
        content = request.form.get('content')
        todo = Todo(content=content,
                    time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
        todo.save(username)
        return redirect(url_for('.todos',username=username))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/<username>/todos/undo/<string:todo_id>')
def todo_undo(username,todo_id):
    if username == session.get('user') and session.get('logged_in'):
        mongo.db.todo.update({'_id':bson.ObjectId(todo_id)},{'$set':{'status':1}})
        return redirect(url_for('.todos',username=username))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/<username>/todos/done/<string:todo_id>')
def todo_done(username,todo_id):
    if username == session.get('user') and session.get('logged_in'):
        mongo.db.todo.update({'_id':bson.ObjectId(todo_id)},{'$set':{'status':0}})
        return redirect(url_for('.todos',username=username))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))

@todo.route('/<username>/todos/delete/<string:todo_id>')
def todo_delete(username,todo_id):
    if username == session.get('user') and session.get('logged_in'):
        mongo.db.todo.remove({'_id':bson.ObjectId(todo_id)})
        mongo.db.user.update({'username':username},{'$pull':{'todos_id':{'_id':bson.ObjectId(todo_id)}}})
        return redirect(url_for('.todos',username=username))
    else:
        flash('请登录先！')
        return redirect(url_for('main.index'))