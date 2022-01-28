import os
import secrets


class Config:

    # general settings
    WTF_CSRF_ENABLED = False
    SECRET_KEY                 = secrets.token_urlsafe()

    # mongodb settings
    MONGODB_DB               = os.environ.get('MONGODB_DB', 'template')
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', 'root')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', 'root')
    MONGODB_HOST                 = os.environ.get('MONGODB_HOST', 'mongo')
    MONGODB_PORT                 = int(os.environ.get('MONGO_PORT', 27017))
    MONGODB_SETTINGS = {
        'host': f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}?authSource={MONGODB_DB}"
    }

    SESSION_TYPE               = os.environ.get('SESSION_TYPE', 'null') # redis perferred?

    # Celery Worker
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')
    C_FORCE_ROOT = True
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]

    IS_ERROR_MAIL_ENABLED = False

    # Flask-Mail Configuration Options
    MAIL_SERVER            = os.getenv('MAIL_SERVER', 'smtp-mail.outlook.com')
    MAIL_PORT              = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS           = os.getenv('MAIL_USE_TLS', True)
    MAIL_USE_SSL           = os.getenv('MAIL_USE_SSL', False)
    MAIL_USERNAME          = os.getenv('MAIL_USERNAME', None)
    MAIL_PASSWORD          = os.getenv('MAIL_PASSWORD', None)
    MAIL_DEFAULT_SENDER    = os.getenv('MAIL_USERNAME', None)
    MAIL_MAX_EMAILS        = os.getenv('MAIL_MAX_EMAILS', None)
    MAIL_SUPPRESS_SEND     = os.getenv('MAIL_MAX_EMAILS', None)
    MAIL_ASCII_ATTACHMENTS = os.getenv('MAIL_MAX_EMAILS', None)


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    EXPLAIN_TEMPLATE_LOADING = True

    SECRET_KEY                 = 'rn4TCYBn25mvaUNkdi-p6XrbwDxcdG6xt72oIXRtOkc'


class TestingConfig(Config):
    TESTING = True
