from flask import Blueprint


blueprint = Blueprint(
    'search_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from .views import blueprint