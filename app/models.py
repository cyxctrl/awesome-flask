from app import app,db
import datetime

class User():
    def __init__(self,username,password,posts=[],todos=[]):
        self.username = username
        self.password = password
        self.posts = posts
        self.todos = todos

    def save(self):
        db.user.insert({'username':self.username,'password':self.password,'posts':self.posts,'todos':self.todos})

class Post():
    def __init__(self,title,text,time=datetime.datetime.now()):
        self.title = title
        self.text = text
        self.time = time

class Todo():
    def __init__(self,content,time=datetime.datetime.now(),status=0):
        self.content = content
        self.time = time
        self.status = status

    def save(self,username):
        db.todo.insert({'content':self.content,'time':self.time,'status':self.status})
        todo_id = db.todo.find_one({'time':self.time},'_id')
        db.user.update({'username':username},{'$push':{'todos':todo_id}})
