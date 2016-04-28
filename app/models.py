#-*- coding: utf-8 -*-
from app import mongo

class User():
    def __init__(self,username,password,register_time,last_login_time,blogs_id=[],todos_id=[]):
        self.username        = username
        self.password        = password
        self.register_time   = register_time
        self.last_login_time = last_login_time
        self.todos_id        = todos_id
        self.blogs_id        = blogs_id

    def save(self):
        mongo.db.user.insert(
            {
                'username':self.username,
                'password':self.password,
                'todos_id':self.todos_id,
                'blogs_id':self.blogs_id,
                'register_time':self.register_time,
                'last_login_time':self.last_login_time
            }
        )

class Todo():
    def __init__(self,content,create_time,status=0):
        self.content     = content
        self.create_time = create_time
        self.status      = status

    def save(self,username):
        mongo.db.todo.insert(
            {
                'content':self.content,
                'create_time':self.create_time,
                'status':self.status
            }
        )

        todo_id = mongo.db.todo.find_one(
            {
                'content':self.content,
                'create_time':self.create_time
            },'_id'
        )['_id']

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
        mongo.db.blog.insert(
            {
                'author':self.author,
                'title':self.title,
                'article':self.article,
                'create_time':self.create_time,
                'last_modify_time':self.last_modify_time,
                'comments_id':self.comments_id
            }
        )

        blog_id = mongo.db.blog.find_one(
            {
                'author':self.author,
                'title':self.title,
                'create_time':self.create_time,
                'last_modify_time':self.last_modify_time
            },'_id'
        )['_id']

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
        mongo.db.comment.insert(
            {
                'author':self.author,
                'content':self.content,
                'create_time':self.create_time
            }
        )

        comment_id = mongo.db.comment.find_one(
            {
                'author':self.author,
                'content':self.content,
                'create_time':self.create_time
            },'_id'
        )['_id']

        mongo.db.blog.update(
            {'_id':blog_id},
            {'$push':{'comments_id':comment_id}}
        )

