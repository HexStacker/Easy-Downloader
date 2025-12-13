"""
Authentication Routes
User registration, login, and token management with email confirmation
"""

from flask import request, jsonify
from . import auth_bp
from .service import AuthService
import logging

logger = logging.getLogger(__name__)
service = AuthService()

def get_client_ip():
    """Get client IP address from request"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
    {
        "username": "user123",
        "email": "user@example.com",
        "confirm_email": "user@example.com",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    }
    """
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        confirm_email = data.get('confirm_email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        # Validate all fields are present
        if not all([username, email, confirm_email, password, confirm_password]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Validate email confirmation
        if email != confirm_email:
            return jsonify({'error': 'Email addresses do not match'}), 400
        
        # Validate password confirmation
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        # Get client IP
        ip_address = get_client_ip()
        
        # Register user
        result = service.register_user(username, email, password, ip_address)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user_id': result.get('user_id')
            }), 201
        else:
            return jsonify({'error': result.get('error')}), 400
            
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user with username or email
    
    Request body:
    {
        "login": "user123 or user@example.com",
        "password": "SecurePass123!"
    }
    """
    try:
        data = request.get_json()
        login = data.get('login')  # Can be username or email
        password = data.get('password')
        
        if not all([login, password]):
            return jsonify({'error': 'Login and password are required'}), 400
        
        # Get client IP
        ip_address = get_client_ip()
        
        # Login user
        result = service.login_user(login, password, ip_address)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'token': result.get('token'),
                'user': result.get('user')
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 401
            
    except Exception as e:
        logger.error(f"Error logging in: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """
    Verify JWT token
    
    Request headers:
    Authorization: Bearer <token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        result = service.verify_token(token)
        
        if result.get('valid'):
            return jsonify({
                'valid': True,
                'user': result.get('user')
            }), 200
        else:
            return jsonify({'error': 'Invalid token'}), 401
            
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (invalidate token)"""
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        service.logout_user(token)
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
            
    except Exception as e:
        logger.error(f"Error logging out: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for auth server"""
    return jsonify({
        'status': 'healthy',
        'service': 'auth-server'
    }), 200

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get user profile
    
    Request headers:
    Authorization: Bearer <token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        result = service.verify_token(token)
        
        if not result.get('valid'):
            return jsonify({'error': 'Invalid token'}), 401
        
        user_info = service.get_user_profile(result['user']['username'])
        
        if user_info:
            return jsonify(user_info), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/activity', methods=['GET'])
def get_activity():
    """
    Get user activity history
    
    Request headers:
    Authorization: Bearer <token>
    
    Query parameters:
    - limit: Number of records (default: 50)
    - offset: Offset for pagination (default: 0)
    - type: Filter by activity type (single, batch, playlist)
    """
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        result = service.verify_token(token)
        
        if not result.get('valid'):
            return jsonify({'error': 'Invalid token'}), 401
        
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        activity_type = request.args.get('type', None)
        
        activities = service.get_user_activity(
            result['user']['username'],
            limit=limit,
            offset=offset,
            activity_type=activity_type
        )
        
        return jsonify({
            'success': True,
            'activities': activities,
            'limit': limit,
            'offset': offset
        }), 200
            
    except Exception as e:
        logger.error(f"Error getting activity: {str(e)}")
        return jsonify({'error': str(e)}), 500
