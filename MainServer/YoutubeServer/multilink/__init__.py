"""
Multi Link Download Module
Handles downloading multiple YouTube videos simultaneously
"""

from flask import Blueprint

multilink_bp = Blueprint('multilink', __name__, url_prefix='/multi')

from . import routes
