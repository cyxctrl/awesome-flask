from app import app
from .models import Todo
from flask import render_template,request
import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/todo')
def todo():
    todos = Todo.objects.order_by('-time')
    return render_template('todo.html',todos=todos)

@app.route('/todo/add',methods=['POST',])
def add():
    content = request.form.get('content')
    time = datetime.datetime.now()
    todo = Todo(content=content,time=time)
    todo.save()
    todos = Todo.objects.order_by('-time')
    return render_template('todo.html',todos=todos)

@app.route('/todo/done/<string:todo_id>')
def done(todo_id):
    todo = Todo.objects.get_or_404(id=todo_id)
    todo.status = 1
    todo.save()
    todos = Todo.objects.order_by('-time')
    return render_template('todo.html',todos=todos)

@app.route('/todo/undo/<string:todo_id>')
def undone(todo_id):
    todo = Todo.objects.get_or_404(id=todo_id)
    todo.status = 0
    todo.save()
    todos = Todo.objects.order_by('-time')
    return render_template('todo.html',todos=todos)

@app.route('/todo/delete/<string:todo_id>')
def delete(todo_id):
    todo = Todo.objects.get_or_404(id=todo_id)
    todo.delete()
    todos = Todo.objects.order_by('-time')
    return render_template('todo.html',todos=todos)