"""
Authentication Server Module
Handles user authentication and authorization
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

from . import routes
