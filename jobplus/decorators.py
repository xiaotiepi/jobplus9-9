from functools import wraps
from .models import User, db
from flask_login import current_user
from flask import abort


def create(role=10):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            user = User()
            user.username = self.username.data
            user.email = self.email.data
            user.password = self.password.data
            user.role = role
            db.session.add(user)
            db.session.commit()
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwrargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(404)
            return func(*args, **kwrargs)

        return wrapper

    return decorator