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
    DEBUG = False
    MONGO_HOST = 'mongo.duapp.com'
    MONGO_PORT = 8908
    MONGO_DBNAME = 'oLNwgqNbtTNsiNjFoDGn'
    MONGO_USERNAME = '07b03aafdcd04c23b8b73ebc0a71ed33'
    MONGO_PASSWORD = '26e4fbac39534a8abcbdc3c7352e7035'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
