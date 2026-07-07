from flask import Blueprint

main_bp = Blueprint('main',__name__)

from app.views import registro_dias_routes
from app.views import cadastro_routes