from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_login import LoginManager # new
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_mongoengine import MongoEngine # new
from flask_mail import Mail
from celery import Celery # new


db = MongoEngine()
bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager() # new
cache = Cache()
session = Session()
mail = Mail()
celery = Celery() # new