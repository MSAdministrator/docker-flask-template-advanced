from functools import wraps
from .base import Base


def log_exception(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in  "
            err += func.__name__
            Base().log_exception(err)
    return wrapper
