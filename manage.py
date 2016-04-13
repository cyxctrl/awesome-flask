# -×- coding: utf-8 -*-
#!flask/bin/python

from flask.ext.script import Manager, Server
from app import app,db
from app.models import User,Todo,Post

manager = Manager(app)

manager.add_command("runserver",
         Server(host='0.0.0.0',port=5000, use_debugger=True))

@manager.command
def save_todo():
    todo = Todo(content="my first todo")
    todo.save()

@manager.command
def add_user():
    user = User('kane','123')
    user.save()

if __name__ == '__main__':
    manager.run()