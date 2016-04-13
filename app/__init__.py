from flask import Flask
import pymongo

app = Flask(__name__)
app.config.from_object('config')

db = pymongo.MongoClient('localhost', 27017).test

from app import views, models