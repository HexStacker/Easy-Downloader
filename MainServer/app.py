"""
Main Server Application
Entry point for the Flask application
"""

from flask import Flask, jsonify
from flask_cors import CORS
import logging
import os

# Import blueprints
from YoutubeServer import youtube_bp
from AuthServer import auth_bp
from DatabaseServer import database_bp


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(youtube_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(database_bp)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Easy Downloader API',
            'version': '2.5.0',
            'services': {
                'youtube': '/api/youtube',
                'auth': '/api/auth',
                'database': '/api/database'
            },
            'endpoints': {
                'youtube_single': '/api/youtube/single',
                'youtube_multi': '/api/youtube/multi',
                'youtube_playlist': '/api/youtube/playlist',
                'auth': '/api/auth',
                'database': '/api/database'
            }
        })
    
    # Health check
    @app.route('/api/health')
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'services': {
                'youtube': 'running',
                'auth': 'running',
                'database': 'running'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    

    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
