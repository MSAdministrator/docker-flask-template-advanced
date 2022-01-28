from flask import Blueprint


blueprint = Blueprint(
    'users_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from .views import blueprint