# -×- coding: utf-8 -*-
#!flask/bin/python
from flask.ext.script import Manager
from app import create_app, mongo

app = create_app('default')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()