"""
YouTube Server Module
Handles YouTube video downloads for single links, multiple links, and playlists
"""

from flask import Blueprint

youtube_bp = Blueprint('youtube', __name__, url_prefix='/api/youtube')

from . import routes
