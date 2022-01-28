from flask import Blueprint


blueprint = Blueprint(
    'home_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from .views import blueprint