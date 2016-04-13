#-*- coding: utf-8 -*-
from app import app, db

class User():
    def __init__(self,username,password,blogs_id=[],todos_id=[]):
        self.username = username
        self.password = password
        self.todos_id = todos_id
        self.blogs_id = blogs_id

    def save(self):
        db.user.insert(
            {'username':self.username,
            'password':self.password,
            'todos_id':self.todos_id,
            'blogs_id':self.blogs_id}
            )

class Todo():
    def __init__(self,content,time,status=0):
        self.content = content
        self.time = time
        self.status = status

    def save(self,username):
        db.todo.insert({'content':self.content,'time':self.time,'status':self.status})
        todo_id = db.todo.find_one({'content':self.content,'time':self.time},'_id')
        db.user.update({'username':username},{'$push':{'todos_id':todo_id}})

class Blog():
    def __init__(self,author,title,content,time,comment_id=[]):
        self.author = author
        self.title = title
        self.content = content
        self.time = time
        self.comments_id = comment_id

class Comment():
    def __init__(self,author,content,time):
        self.author = author
        self.content = content
        self.time = time