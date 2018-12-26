import os
<<<<<<< HEAD

=======
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
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
<<<<<<< HEAD
=======
    ADMIN_PER_PAGE=10
    @staticmethod
    def init_app(app):
        pass
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOP_DATABASE_URL") or DB_URI


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
