#-*- coding: utf-8 -*-
from app import mongo
from flask.ext.login import UserMixin
from . import login_manager

class User(UserMixin):
    def __init__(self,username,password,email,register_time,last_login_time,blogs_id=[],todos_id=[],markdown_id=[]):
        self.email           = email
        self.username        = username
        self.password        = password
        self.register_time   = register_time
        self.last_login_time = last_login_time
        self.todos_id        = todos_id
        self.blogs_id        = blogs_id
        self.markdown_id     = markdown_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def save(self):
        mongo.db.user.insert(
            {
                'email':self.email,
                'username':self.username,
                'password':self.password,
                'todos_id':self.todos_id,
                'blogs_id':self.blogs_id,
                'register_time':self.register_time,
                'last_login_time':self.last_login_time
            }
        )

        markdown_id = mongo.db.markdown.save({'text':''})

        mongo.db.user.update(
            {'username':self.username},
            {'$push':{'markdown_id':markdown_id}}
        )

@login_manager.user_loader
def load_user(username):
    user = mongo.db.user.find_one({"username": username})
    if not user:
        return None
    return User(user['username'],
                user['password'],
                user['email'],
                user['register_time'],
                user['last_login_time'])

class Todo():
    def __init__(self,content,create_time,status=0):
        self.content     = content
        self.create_time = create_time
        self.status      = status

    def save(self,username):
        todo_id = mongo.db.todo.save(
            {
                'content':self.content,
                'create_time':self.create_time,
                'status':self.status
            }
        )

        mongo.db.user.update(
            {'username':username},
            {'$push':{'todos_id':todo_id}}
        )

class Blog():
    def __init__(self,author,title,create_time,last_modify_time,article,comments_id=[]):
        self.author           = author
        self.title            = title
        self.create_time      = create_time
        self.last_modify_time = last_modify_time
        self.article          = article
        self.comments_id      = comments_id

    def save(self,username):
        blog_id = mongo.db.blog.save(
            {
                'author':self.author,
                'title':self.title,
                'article':self.article,
                'create_time':self.create_time,
                'last_modify_time':self.last_modify_time,
                'comments_id':self.comments_id
            }
        )

        mongo.db.user.update(
            {'username':username},
            {'$push':{'blogs_id':blog_id}}
        )

class Comment():
    def __init__(self,author,content,create_time):
        self.author      = author
        self.content     = content
        self.create_time = create_time

    def save(self,blog_id):
        comment_id = mongo.db.comment.save(
            {
                'author':self.author,
                'content':self.content,
                'create_time':self.create_time
            }
        )

        mongo.db.blog.update(
            {'_id':blog_id},
            {'$push':{'comments_id':comment_id}}
        )
