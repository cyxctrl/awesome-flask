#-*- coding: utf-8 -*-

class Config():
    SECRET_KEY = 'development key'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'awesome_flask'

class ProductionConfig(Config):
    MONGO_HOST = 'mongo.duapp.com'
    MONGO_PORT = 8909
    MONGO_DBNAME = 'oLNwgqNbtTNsiNjFoDGn'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


#db = pymongo.MongoClient('localhost', 27017).awesome_flask
#db = pymongo.MongoClient("mongo.duapp.com", 8908).oLNwgqNbtTNsiNjFoDGn