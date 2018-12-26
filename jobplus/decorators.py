from functools import wraps
from .models import User, db


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
