#-*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session, flash
from . import main

@main.route('/test')
def test():
    return render_template('editor.html')

@main.route('/')
def index():
    if session.get('logged_in'):
        username = session.get('user')
        return redirect(url_for('profile.user',username=username))
    return render_template('index.html')

'''
@main.teardown_request
def teardown_request(exception):
    pymongo.MongoClient('localhost',27017).close()
    #pymongo.MongoClient("mongo.duapp.com", 8908).close()
'''






