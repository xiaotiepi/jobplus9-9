import os

HOSTNAME = '127.0.0.1'
PORT = "3306"
DATABASE = "plus_job"
USERNAME = "root"


DB_URI = "mysql://{}@{}:{}/{}?charset=utf8".format(USERNAME, HOSTNAME, PORT, DATABASE)






class BaseConfig(object):
    SECRET_KEY = "2018xxxxx"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    COMPANY_PER_PAGE = 9
    JOB_PER_PAGE = 9


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOP_DATABASE_URL") or DB_URI


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
