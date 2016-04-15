#-*- coding: utf-8 -*-
from app import app, db
from flask import render_template,request,redirect,url_for,session,flash
from .models import User, Todo, Blog, Comment
import pymongo
import bson
import datetime
import os

@app.route('/test')
def test():
    return render_template('editor.html')

@app.route('/')
def index():
    if session.get('user'):
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
        blogs_id = db.user.find_one({'username':username})['blogs_id']
        blog_list = []
        for bid in blogs_id:
            bg = db.blog.find_one(bid)
            blog_list.append(bg)
        return render_template('user.html',username=username,blog_list=blog_list[::-1])
    return redirect(url_for('index'))

@app.route('/<username>/todos')
def todos(username):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    todos_id = db.user.find_one({'username':username})['todos_id']
    todo_list = []
    for tid in todos_id:
        td = db.todo.find_one(tid)
        todo_list.append(td)
    return render_template('todos.html',todo_list=todo_list[::-1])

@app.route('/<username>/todos/add',methods=['POST',])
def todo_add(username):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    content = request.form.get('content')
    todo = Todo(content=content,
                time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
    todo.save(username)
    return redirect(url_for('todos'))

@app.route('/<username>/todos/undo/<string:todo_id>')
def todo_undo(username,todo_id):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    db.todo.update({'_id':bson.ObjectId(todo_id)},{'$set':{'status':1}})
    return redirect(url_for('todos'))

@app.route('/<username>/todos/done/<string:todo_id>')
def todo_done(username,todo_id):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    db.todo.update({'_id':bson.ObjectId(todo_id)},{'$set':{'status':0}})
    return redirect(url_for('todos'))

@app.route('/<username>/todos/delete/<string:todo_id>')
def todo_delete(username,todo_id):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    db.todo.remove({'_id':bson.ObjectId(todo_id)})
    db.user.update({'username':username},{'$pull':{'todos_id':{'_id':bson.ObjectId(todo_id)}}})
    return redirect(url_for('todos'))

@app.route('/article/<string:blog_id>')
def article(blog_id):
    blog = db.blog.find_one({'_id':bson.ObjectId(blog_id)})
    username = session.get('user')
    return render_template('article.html',blog=blog)

@app.route('/editor_add')
def editor_add():
    username = session.get('user')
    return render_template('editor_add.html',username=username)

@app.route('/<username>/blogs/add',methods=['POST',])
def blog_add(username):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    title = request.form['title']
    article = request.form['article']
    blog = Blog(author=session.get('user'),
                title=title,
                article=article,
                time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
    blog.save(username)
    return redirect(url_for('user',username=username))

@app.route('/editor_modify/<string:blog_id>')
def editor_modify(blog_id):
    blog = db.blog.find_one({'_id':bson.ObjectId(blog_id)})
    blog_id = str(blog['_id'])
    title = blog['title']
    article = blog['article']
    username = session.get('user')
    return render_template('editor_modify.html',blog_id=blog_id,title=title,article=article,username=username)

@app.route('/<username>/blogs/modify/<string:blog_id>',methods=['POST',])
def blog_modify(username,blog_id):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    title = request.form['title']
    article = request.form['article']
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.blog.update({'_id':bson.ObjectId(blog_id)},{'$set':{'title':title,'article':article,'time':time}})
    return redirect(url_for('user',username=username))

@app.route('/<username>/blogs/delete/<string:blog_id>')
def blog_delete(username,blog_id):
    if session.get('user') != username:
        flash('请登录先！')
        return redirect('index')
    db.blog.remove({'_id':bson.ObjectId(blog_id)})
    db.user.update({'username':username},{'$pull':{'blogs_id':{'_id':bson.ObjectId(blog_id)}}})
    return redirect(url_for('user',username=username))