"""
Authentication Service
Business logic for user authentication with strong password validation
"""

import os
import jwt
import bcrypt
import re
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication"""
    
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
        self.algorithm = 'HS256'
        self.token_expiry = timedelta(days=7)
        self.users = {}  # In-memory storage, will be replaced with DB
        self.blacklisted_tokens = set()  # Token blacklist for logout
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password_strength(self, password):
        """
        Validate password strength
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
        
        return True, "Password is strong"
    
    def validate_username(self, username):
        """
        Validate username
        Requirements:
        - 3-20 characters
        - Only letters, numbers, and underscores
        """
        if len(username) < 3 or len(username) > 20:
            return False, "Username must be between 3 and 20 characters"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, "Username is valid"
    
    def register_user(self, username, email, password, ip_address):
        """
        Register a new user with validation
        
        Args:
            username: User's username
            email: User's email
            password: User's password (plain text, will be hashed)
            ip_address: User's IP address
            
        Returns:
            dict: Registration result
        """
        try:
            # Validate username
            valid, message = self.validate_username(username)
            if not valid:
                return {'success': False, 'error': message}
            
            # Validate email
            if not self.validate_email(email):
                return {'success': False, 'error': 'Invalid email format'}
            
            # Validate password strength
            valid, message = self.validate_password_strength(password)
            if not valid:
                return {'success': False, 'error': message}
            
            # Check if username already exists
            if username in self.users:
                return {'success': False, 'error': 'Username already exists'}
            
            # Check if email already exists
            for user in self.users.values():
                if user['email'] == email:
                    return {'success': False, 'error': 'Email already exists'}
            
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user
            user_id = len(self.users) + 1
            self.users[username] = {
                'id': user_id,
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'created_at': datetime.utcnow().isoformat(),
                'registration_ip': ip_address,
                'last_login_ip': None,
                'last_login_at': None,
                'is_active': True
            }
            
            logger.info(f"User registered: {username} from IP {ip_address}")
            
            return {
                'success': True,
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def login_user(self, login, password, ip_address):
        """
        Login user with username or email
        
        Args:
            login: Username or email
            password: User's password
            ip_address: User's IP address
            
        Returns:
            dict: Login result with token
        """
        try:
            # Find user by username or email
            user = None
            username_key = None
            
            # Check if login is email
            if '@' in login:
                for uname, udata in self.users.items():
                    if udata['email'] == login:
                        user = udata
                        username_key = uname
                        break
            else:
                # Login is username
                if login in self.users:
                    user = self.users[login]
                    username_key = login
            
            if not user:
                return {'success': False, 'error': 'Invalid credentials'}
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
                return {'success': False, 'error': 'Invalid credentials'}
            
            # Check if user is active
            if not user.get('is_active', True):
                return {'success': False, 'error': 'Account is inactive'}
            
            # Update last login info
            user['last_login_at'] = datetime.utcnow().isoformat()
            user['last_login_ip'] = ip_address
            
            # Generate JWT token
            token = self._generate_token(user)
            
            logger.info(f"User logged in: {user['username']} from IP {ip_address}")
            
            return {
                'success': True,
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            }
            
        except Exception as e:
            logger.error(f"Error logging in: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _generate_token(self, user):
        """Generate JWT token for user"""
        payload = {
            'user_id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'exp': datetime.utcnow() + self.token_expiry,
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token):
        """
        Verify JWT token
        
        Args:
            token: JWT token
            
        Returns:
            dict: Verification result with user data
        """
        try:
            # Check if token is blacklisted
            if token in self.blacklisted_tokens:
                return {'valid': False, 'error': 'Token has been revoked'}
            
            # Decode token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            return {
                'valid': True,
                'user': {
                    'id': payload['user_id'],
                    'username': payload['username'],
                    'email': payload['email']
                }
            }
            
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Invalid token'}
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return {'valid': False, 'error': str(e)}
    
    def logout_user(self, token):
        """
        Logout user by blacklisting token
        
        Args:
            token: JWT token to blacklist
        """
        self.blacklisted_tokens.add(token)
    
    def get_user_by_username(self, username):
        """Get user by username"""
        return self.users.get(username)
    
    def get_user_profile(self, username):
        """
        Get user profile information
        
        Args:
            username: User's username
            
        Returns:
            dict: User profile data
        """
        user = self.users.get(username)
        if not user:
            return None
        
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'registration_ip': user.get('registration_ip'),
            'last_login_at': user.get('last_login_at'),
            'last_login_ip': user.get('last_login_ip'),
            'is_active': user.get('is_active', True),
            'total_downloads': len(user.get('activities', []))
        }
    
    def log_user_activity(self, username, activity_data):
        """
        Log user activity (download)
        
        Args:
            username: User's username
            activity_data: dict containing:
                - activity_type: 'single', 'batch', or 'playlist'
                - download_id: ID of the download
                - url: Download URL
                - title: Video/playlist title
                - format: mp4 or mp3
                - quality: Video quality
                - ip_address: User's IP address
                - status: Download status
                - file_size: File size in bytes (optional)
                - user_agent: Browser/client info (optional)
        
        Returns:
            dict: Activity log result
        """
        try:
            user = self.users.get(username)
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            # Initialize activities list if not exists
            if 'activities' not in user:
                user['activities'] = []
            
            # Create activity record
            activity = {
                'id': len(user['activities']) + 1,
                'activity_type': activity_data.get('activity_type'),
                'download_id': activity_data.get('download_id'),
                'url': activity_data.get('url'),
                'title': activity_data.get('title'),
                'format': activity_data.get('format'),
                'quality': activity_data.get('quality'),
                'status': activity_data.get('status', 'pending'),
                'ip_address': activity_data.get('ip_address'),
                'created_at': datetime.utcnow().isoformat(),
                'completed_at': activity_data.get('completed_at'),
                'file_size': activity_data.get('file_size'),
                'user_agent': activity_data.get('user_agent')
            }
            
            user['activities'].append(activity)
            
            logger.info(f"Activity logged for user {username}: {activity_data.get('activity_type')} - {activity_data.get('url')}")
            
            return {
                'success': True,
                'activity_id': activity['id']
            }
            
        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_user_activity(self, username, limit=50, offset=0, activity_type=None):
        """
        Get user activity history
        
        Args:
            username: User's username
            limit: Number of records to return
            offset: Offset for pagination
            activity_type: Filter by activity type (optional)
            
        Returns:
            list: User activities
        """
        try:
            user = self.users.get(username)
            if not user:
                return []
            
            activities = user.get('activities', [])
            
            # Filter by activity type if specified
            if activity_type:
                activities = [a for a in activities if a.get('activity_type') == activity_type]
            
            # Sort by created_at descending (newest first)
            activities = sorted(activities, key=lambda x: x.get('created_at', ''), reverse=True)
            
            # Apply pagination
            start = offset
            end = offset + limit
            
            return activities[start:end]
            
        except Exception as e:
            logger.error(f"Error getting user activity: {str(e)}")
            return []
    
    def update_activity_status(self, username, download_id, status, completed_at=None, file_size=None):
        """
        Update activity status when download completes/fails
        
        Args:
            username: User's username
            download_id: Download ID
            status: New status
            completed_at: Completion timestamp (optional)
            file_size: File size in bytes (optional)
        """
        try:
            user = self.users.get(username)
            if not user or 'activities' not in user:
                return
            
            for activity in user['activities']:
                if activity.get('download_id') == download_id:
                    activity['status'] = status
                    if completed_at:
                        activity['completed_at'] = completed_at
                    if file_size:
                        activity['file_size'] = file_size
                    break
                    
        except Exception as e:
            logger.error(f"Error updating activity status: {str(e)}")
