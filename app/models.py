#-*- coding: utf-8 -*-
from app import mongo
import datetime
from flask.ext.login import UserMixin
from . import login_manager

class User():
    def __init__(self,username,password,email,register_time,last_login_time,
                permission=5,location='',about_me=u'这个人比较懒，还没有填写个人简介。',
                blogs_id=[],todos_id=[],markdown_id=[],following=[]):
        self.email           = email
        self.username        = username
        self.password        = password
        self.register_time   = register_time
        self.last_login_time = last_login_time
        self.permission      = permission
        self.location        = location
        self.about_me        = about_me
        self.todos_id        = todos_id
        self.blogs_id        = blogs_id
        self.markdown_id     = markdown_id
        self.following       = following

    def save(self):
        mongo.db.user.insert(
            {
                'email':self.email,
                'username':self.username,
                'password':self.password,
                'todos_id':self.todos_id,
                'blogs_id':self.blogs_id,
                'markdown_id':self.markdown_id,
                'register_time':self.register_time,
                'last_login_time':self.last_login_time,
                'permission':self.permission,
                'location':self.location,
                'about_me':self.about_me,
                'following':self.following
            }
        )

        markdown_id = mongo.db.markdown.save({'text':''})

        mongo.db.user.update(
            {'username':self.username},
            {'$push':{'markdown_id':markdown_id}}
        )

class CurrentUser(UserMixin):
    def __init__(self,username,email,permission,blogs_id,todos_id,markdown_id,following):
        self.email       = email
        self.username    = username
        self.permission  = permission
        self.todos_id    = todos_id
        self.blogs_id    = blogs_id
        self.markdown_id = markdown_id
        self.following   = following

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    user = mongo.db.user.find_one({"username": username})
    if not user:
        return None
    return CurrentUser(
                username    = user['username'],
                email       = user['email'],
                permission  = user['permission'],
                blogs_id    = user['blogs_id'],
                todos_id    = user['todos_id'],
                markdown_id = user['markdown_id'],
                following   = user['following']
                )

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
    def __init__(self,author,title,create_time,last_modify_time,article,permission,comments_id=[]):
        self.author           = author
        self.title            = title
        self.create_time      = create_time
        self.last_modify_time = last_modify_time
        self.article          = article
        self.permission = permission
        self.comments_id      = comments_id

    def save(self,username):
        blog_id = mongo.db.blog.save(
            {
                'author':self.author,
                'title':self.title,
                'article':self.article,
                'permission':self.permission,
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
