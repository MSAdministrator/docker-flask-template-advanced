
# import external packages
from flask import (
    Flask, 
    render_template, 
    g
)
from flask_bootstrap import Bootstrap4
from celery import Celery # new


# Import extensions
from template.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    login_manager, # new
    db # new
)

# Import routes
from template.blueprints import (
    home,
    users,
    search
)

### Instantiate Config ###
from template.config import Config
config = Config()

# used for tasks and workers
celery = Celery(
    __name__,
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND
)


from flask_mail import Mail
mail = Mail()


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(home.views.blueprint)
    app.register_blueprint(users.views.blueprint)
    app.register_blueprint(search.views.blueprint)
    return None

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app) # new
    csrf_protect.init_app(app)
    login_manager.init_app(app) # new
    mail.init_app(app)
    Bootstrap4(app)
    return None

def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

def configure_logging(app):
    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler

    # Deactivate the default flask logger so that log messages don't get duplicated 
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler('app.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)

def register_error_handlers(app):
    
    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

def register_db_connections(app):
    """If using a database like MongoDB 
    you can register special decorators
    that will run before, after, and the 
    teardown of an API endpoint request
    """
    from template.database import database_session # new

    @app.before_request
    def before_request():
        g.db = database_session.database # new

    @app.after_request
    def after_request(response):
        database_session.client.close() # new
        return response

    @app.teardown_request
    def teardown_request(exception):
        database_session.client.close() # new


def create_app():
    """Create application factory
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config)

    with app.app_context():
        register_extensions(app)
        register_blueprints(app)
        register_errorhandlers(app)
        register_db_connections(app)
        return app
