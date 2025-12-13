"""
Single Link Download Module
Handles downloading individual YouTube videos
"""

from flask import Blueprint

singlelink_bp = Blueprint('singlelink', __name__, url_prefix='/single')

from . import routes
