
HOSTNAME = '127.0.0.1'
<<<<<<< HEAD:jobplus/config.py
DB_PORT = "3306"
DATABASE = "plus_job"
USERNAME = "root"
PASSWORD = 'puhao'
DB_URI = "mysql://{}:{}@{}:{}?charset=utf8".format(USERNAME, PASSWORD, HOSTNAME, DB_PORT, DATABASE)
=======
PORT = "3306"
DATABASE = "plus_job"
USERNAME = "root"
# PASSWORD = 'puhao'
DB_URI = "mysql://{}@{}:{}/{}?charset=utf8".format(USERNAME, HOSTNAME, PORT, DATABASE)
>>>>>>> c7594099b2a2393673df70a3d93aaf9dbdefa064:jobplus/jobplus/config.py


class BaseConfig(object):
    SECRET_KEY = "2018xxxxx"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DB_URI


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
