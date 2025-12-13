"""
Database Server Module
Handles PostgreSQL database connections and operations
"""

from flask import Blueprint

database_bp = Blueprint('database', __name__, url_prefix='/api/database')

from . import routes
