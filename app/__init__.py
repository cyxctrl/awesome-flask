#-*- coding: utf-8 -*-
from flask import Flask
import pymongo

app = Flask(__name__)
app.config.from_object('config')

db = pymongo.MongoClient('localhost', 27017).awesome_flask

#db = pymongo.MongoClient("mongo.duapp.com", 8908).oLNwgqNbtTNsiNjFoDGn

from app import views, models