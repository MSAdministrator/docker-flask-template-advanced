from hashlib import md5

import pendulum
from flask_login import UserMixin
from flask import current_app
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from itsdangerous import (
    URLSafeSerializer, 
    URLSafeTimedSerializer
)
from template.app import (
    db, 
    login_manager
)


@login_manager.user_loader
def load_user(id):
    return User.objects.get(id=id)


class User(db.Document, UserMixin):
    name = db.StringField(required=True)
    username = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    registered_on = db.DateTimeField(default=pendulum.now(), required=True)
    confirmed = db.BooleanField(nullable=False, default=False)
    confirmed_at = db.DateTimeField()
    last_seen = db.DateTimeField()
    last_ip = db.StringField()
    is_admin = db.BooleanField(nullable=False, default=False)
    is_authenticated = db.BooleanField(nullable=False, default=False)
    is_active = db.BooleanField(nullable=False, default=True)

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.is_active

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    @staticmethod
    def is_anonymous():
        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_token(self, salt):
        serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(
            self.email,
            salt=salt
        )

    def decode_token(self, token, salt, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token, 
                salt=salt,
                max_age=expiration
            )
            return email
        except:
            return False

    def get_json(self):
        return {
            'name': self.name,
            'username': self.username,
            'email': self.email,
        }
