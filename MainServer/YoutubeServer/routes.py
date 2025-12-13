"""
YouTube Server Routes
Main routing file that delegates to specific modules
"""

from flask import jsonify
from . import youtube_bp
from .singlelink import routes as singlelink_routes
from .multilink import routes as multilink_routes
from .playlist import routes as playlist_routes

# Register sub-routes
youtube_bp.register_blueprint(singlelink_routes.singlelink_bp)
youtube_bp.register_blueprint(multilink_routes.multilink_bp)
youtube_bp.register_blueprint(playlist_routes.playlist_bp)

@youtube_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for YouTube server"""
    return jsonify({
        'status': 'healthy',
        'service': 'youtube-server',
        'modules': ['singlelink', 'multilink', 'playlist']
    }), 200
