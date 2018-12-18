from flask import Flask, redirect, render_template
from .config import configs
from flask_migrate import Migrate
from .models import db


def register_blueprints(app):
    from .handlers import front, admin, company, job, user
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(company)
    app.register_blueprint(job)
    app.register_blueprint(user)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    Migrate(app=app, db=db)
    register_blueprints(app)
    return app
