#-*- coding: utf-8 -*-
from app import mongo

class User():
    def __init__(self,username,password,blogs_id=[],todos_id=[]):
        self.username = username
        self.password = password
        self.todos_id = todos_id
        self.blogs_id = blogs_id

    def save(self):
        mongo.db.user.insert(
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
        mongo.db.todo.insert({'content':self.content,'time':self.time,'status':self.status})
        todo_id = mongo.db.todo.find_one({'content':self.content,'time':self.time},'_id')
        mongo.db.user.update({'username':username},{'$push':{'todos_id':todo_id}})

class Blog():
    def __init__(self,author,title,article,time,comments_id=[]):
        self.author = author
        self.title = title
        self.article = article
        self.time = time
        self.comments_id = comments_id

    def save(self,username):
        mongo.db.blog.insert({'author':self.author,'title':self.title,'article':self.article,'time':self.time,'comments_id':self.comments_id})
        blog_id = mongo.db.blog.find_one({'author':username,'title':self.title,'time':self.time},'_id')
        mongo.db.user.update({'username':username},{'$push':{'blogs_id':blog_id}})

class Comment():
    def __init__(self,author,content,time):
        self.author = author
        self.content = content
        self.time = time