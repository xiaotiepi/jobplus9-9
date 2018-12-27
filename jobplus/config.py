import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTNAME = '127.0.0.1'
PORT = "3306"
DATABASE = "plus_job"
USERNAME = "root"
DB_URI = "mysql://{}@{}:{}/{}?charset=utf8".format(USERNAME, HOSTNAME, PORT, DATABASE)
# DB_URI = 'mysql://xiaotiepi:12580@localhost:3306/plus_job?charset=utf8'


class BaseConfig(object):
    SECRET_KEY = "2018xxxxx"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    COMPANY_PER_PAGE = 9
    JOB_PER_PAGE = 9
    ADMIN_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


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
