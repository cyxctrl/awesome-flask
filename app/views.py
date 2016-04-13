from app import app,db
from flask import render_template,request,redirect,url_for,session,flash
from .models import User,Todo,Post
import pymongo
import bson
import datetime

@app.route('/')
def index():
    if session.get('logged_in') == True:
        return redirect(url_for('user',username=session.get('user')))
    return render_template('index.html')

@app.teardown_request
def teardown_request(exception):
    pymongo.MongoClient('localhost',27017).close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/register',methods=['POST','GET'])
def register():
    username_register = request.form['username']
    password_register = request.form['password']
    if request.method == 'POST':
        if db.user.find_one({'username':username_register}):
            flash('用户名已存在！')
            return redirect(url_for('index'))
        user = User(username=username_register,password=password_register)
        user.save()
        flash('注册成功！')
        return redirect(url_for('index'))
    flash('出错了？')
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    username_login = request.form['username']
    password_login = request.form['password']
    if request.method == 'POST':
        if db.user.find_one({'username':username_login,'password':password_login}):
            session['logged_in'] = True
            session['user'] = username_login
            return redirect(url_for('index'))
    flash('用户不存在？账号错误？密码错误？')
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('注销成功！')
    return redirect(url_for('index'))

@app.route('/<username>')
def user(username):
    if username == session.get('user'):
        return render_template('user.html',username=username)
    return redirect(url_for('index'))

@app.route('/<username>/todo')
def todo(username):
    todos_id = db.user.find_one({'username':username})['todos']
    todo_list = []
    for tid in todos_id:
        td = db.todo.find_one(tid)
        todo_list.append(td)
    return render_template('todo.html',todo_list=todo_list,username=username)

@app.route('/<username>/todo/add',methods=['POST',])
def add(username):
    content = request.form.get('content')
    time = datetime.datetime.now()
    todo = Todo(content=content,time=time)
    todo.save(username)
    return redirect(url_for('todo',username=username))

@app.route('/<username>/todo/undo/<string:todo_id>')
def undo(username,todo_id):
    db.todo.update({'_id':bson.ObjectId(todo_id)},{'$set':{'status':1}})
    return redirect(url_for('todo',username=username))

@app.route('/<username>/todo/done/<string:todo_id>')
def done(username,todo_id):
    db.todo.update({'_id':bson.ObjectId(todo_id)},{'$set':{'status':0}})
    return redirect(url_for('todo',username=username))

@app.route('/<username>/todo/delete/<string:todo_id>')
def delete(username,todo_id):
    db.todo.remove({'_id':bson.ObjectId(todo_id)})
    db.user.update({'username':username},{'$pull':{'todos':{'_id':bson.ObjectId(todo_id)}}})
    return redirect(url_for('todo',username=username))
