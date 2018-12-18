
HOSTNAME = '12.0.0.1'
PORT = "3306"
DATABASE = "plus_job"
USERNAME = "root"
PASSWORD = 'puhao'
DB_URI = "mysql://{}:{}@{}:{}?charset=utf8".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)


class BaseConfig(object):
    SECRET_KEY = "2018xxxxx"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
