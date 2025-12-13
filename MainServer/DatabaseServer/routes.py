"""
Database Routes
Health check and database management endpoints
"""

from flask import jsonify
from . import database_bp
from .config import engine, init_db
from sqlalchemy import text

@database_bp.route('/health', methods=['GET'])
def health_check():
    """Check database connection health"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        
        return jsonify({
            'status': 'healthy',
            'service': 'database-server',
            'database': 'postgresql',
            'connected': True
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'database-server',
            'database': 'postgresql',
            'connected': False,
            'error': str(e)
        }), 500

@database_bp.route('/init', methods=['POST'])
def initialize_database():
    """Initialize database tables"""
    try:
        init_db()
        return jsonify({
            'success': True,
            'message': 'Database tables created successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
