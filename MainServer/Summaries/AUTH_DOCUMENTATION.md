# Authentication System Documentation

## 🔐 Overview

The authentication system provides secure user registration, login, and activity tracking with the following features:

- **Strong Password Requirements**
- **Email Confirmation**
- **Flexible Login** (username or email)
- **IP Address Tracking**
- **Download History Tracking**
- **JWT Token Authentication**

---

## 📋 Registration Requirements

### Username
- **Length**: 3-20 characters
- **Allowed characters**: Letters, numbers, and underscores only
- **Examples**: 
  - ✅ `john_doe`, `user123`, `JohnDoe`
  - ❌ `ab` (too short), `john-doe` (hyphen not allowed), `user@123` (@ not allowed)

### Email
- Must be a valid email format
- Must be unique (not already registered)
- Must match confirmation email
- **Examples**:
  - ✅ `user@example.com`, `john.doe@company.co.uk`
  - ❌ `invalid-email`, `user@`, `@example.com`

### Password (Strong Requirements)
- **Minimum 8 characters**
- **At least one uppercase letter** (A-Z)
- **At least one lowercase letter** (a-z)
- **At least one number** (0-9)
- **At least one special character** (!@#$%^&*(),.?":{}|<>)
- Must match confirmation password

**Examples**:
- ✅ `SecurePass123!`, `MyP@ssw0rd`, `Test#1234Abc`
- ❌ `password` (no uppercase, number, or special char)
- ❌ `PASSWORD123` (no lowercase or special char)
- ❌ `Pass1!` (too short)

---

## 🌐 API Endpoints

### 1. Register User

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "confirm_email": "john@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Success Response (201)**:
```json
{
  "success": true,
  "message": "User registered successfully",
  "user_id": 1
}
```

**Error Responses (400)**:
```json
// Missing fields
{"error": "All fields are required"}

// Email mismatch
{"error": "Email addresses do not match"}

// Password mismatch
{"error": "Passwords do not match"}

// Weak password
{"error": "Password must contain at least one uppercase letter"}

// Invalid username
{"error": "Username must be between 3 and 20 characters"}

// Duplicate username
{"error": "Username already exists"}

// Duplicate email
{"error": "Email already exists"}
```

---

### 2. Login User

```http
POST /api/auth/login
Content-Type: application/json

{
  "login": "john_doe",  // Can be username OR email
  "password": "SecurePass123!"
}
```

**Login with Email**:
```json
{
  "login": "john@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Error Responses (401)**:
```json
// Invalid credentials
{"error": "Invalid credentials"}

// Inactive account
{"error": "Account is inactive"}
```

---

### 3. Verify Token

```http
POST /api/auth/verify
Authorization: Bearer <your-jwt-token>
```

**Success Response (200)**:
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Error Responses (401)**:
```json
// Invalid header
{"error": "Invalid authorization header"}

// Expired token
{"error": "Token has expired"}

// Invalid token
{"error": "Invalid token"}

// Revoked token
{"error": "Token has been revoked"}
```

---

### 4. Logout User

```http
POST /api/auth/logout
Authorization: Bearer <your-jwt-token>
```

**Success Response (200)**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### 5. Get User Profile

```http
GET /api/auth/profile
Authorization: Bearer <your-jwt-token>
```

**Success Response (200)**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-12-12T18:30:00.000Z",
  "registration_ip": "192.168.1.100",
  "last_login_at": "2025-12-12T19:00:00.000Z",
  "last_login_ip": "192.168.1.101",
  "is_active": true,
  "total_downloads": 15
}
```

---

### 6. Get User Activity History

```http
GET /api/auth/activity?limit=50&offset=0&type=single
Authorization: Bearer <your-jwt-token>
```

**Query Parameters**:
- `limit` (optional): Number of records (default: 50)
- `offset` (optional): Pagination offset (default: 0)
- `type` (optional): Filter by type (`single`, `batch`, `playlist`)

**Success Response (200)**:
```json
{
  "success": true,
  "activities": [
    {
      "id": 1,
      "activity_type": "single",
      "download_id": "abc-123-def",
      "url": "https://youtube.com/watch?v=...",
      "title": "Video Title",
      "format": "mp4",
      "quality": "720p",
      "status": "completed",
      "ip_address": "192.168.1.100",
      "created_at": "2025-12-12T18:45:00.000Z",
      "completed_at": "2025-12-12T18:46:30.000Z",
      "file_size": 52428800,
      "user_agent": "Mozilla/5.0..."
    },
    {
      "id": 2,
      "activity_type": "playlist",
      "download_id": "xyz-456-ghi",
      "url": "https://youtube.com/playlist?list=...",
      "title": "My Playlist",
      "format": "mp4",
      "quality": "1080p",
      "status": "downloading",
      "ip_address": "192.168.1.100",
      "created_at": "2025-12-12T19:00:00.000Z",
      "completed_at": null,
      "file_size": null,
      "user_agent": "Mozilla/5.0..."
    }
  ],
  "limit": 50,
  "offset": 0
}
```

---

## 🔒 Security Features

### 1. Password Hashing
- Uses **bcrypt** for secure password hashing
- Automatic salt generation
- Passwords are never stored in plain text

### 2. JWT Tokens
- **7-day expiration** by default
- Contains user ID, username, and email
- Signed with secret key
- Token blacklisting on logout

### 3. IP Address Tracking
- **Registration IP**: Recorded when user registers
- **Login IP**: Updated on each login
- **Activity IP**: Recorded for each download

### 4. Input Validation
- Email format validation
- Username format validation
- Strong password requirements
- SQL injection prevention (when using database)

---

## 📊 User Activity Tracking

Every download is automatically tracked with:

- **Activity Type**: single, batch, or playlist
- **Download ID**: Reference to the download
- **URL**: Original video/playlist URL
- **Title**: Video or playlist title
- **Format**: mp4 or mp3
- **Quality**: Video quality setting
- **Status**: pending, downloading, completed, failed, cancelled
- **IP Address**: User's IP at time of download
- **Timestamp**: When download was initiated
- **Completion Time**: When download finished
- **File Size**: Size of downloaded file
- **User Agent**: Browser/client information

---

## 💾 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    registration_ip VARCHAR(50),
    last_login_ip VARCHAR(50),
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### User Activities Table
```sql
CREATE TABLE user_activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    activity_type VARCHAR(20) NOT NULL,  -- single, batch, playlist
    download_id VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    title VARCHAR(500),
    format VARCHAR(10),  -- mp4, mp3
    quality VARCHAR(20),  -- best, 720p, etc.
    status VARCHAR(20) DEFAULT 'pending',
    ip_address VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    file_size INTEGER,
    user_agent VARCHAR(500)
);
```

---

## 📝 Usage Examples

### Python Example

```python
import requests

BASE_URL = "http://localhost:5000/api/auth"

# 1. Register
register_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "confirm_email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!"
}

response = requests.post(f"{BASE_URL}/register", json=register_data)
print(response.json())

# 2. Login
login_data = {
    "login": "john_doe",  # or "john@example.com"
    "password": "SecurePass123!"
}

response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()['token']
print(f"Token: {token}")

# 3. Get Profile
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/profile", headers=headers)
print(response.json())

# 4. Get Activity History
response = requests.get(
    f"{BASE_URL}/activity?limit=10&type=single",
    headers=headers
)
print(response.json())
```

### JavaScript Example

```javascript
const BASE_URL = "http://localhost:5000/api/auth";

// 1. Register
async function register() {
  const response = await fetch(`${BASE_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'john_doe',
      email: 'john@example.com',
      confirm_email: 'john@example.com',
      password: 'SecurePass123!',
      confirm_password: 'SecurePass123!'
    })
  });
  return await response.json();
}

// 2. Login
async function login() {
  const response = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      login: 'john_doe',
      password: 'SecurePass123!'
    })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data;
}

// 3. Get Profile
async function getProfile() {
  const token = localStorage.getItem('token');
  const response = await fetch(`${BASE_URL}/profile`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
}

// 4. Get Activity
async function getActivity(limit = 50, type = null) {
  const token = localStorage.getItem('token');
  let url = `${BASE_URL}/activity?limit=${limit}`;
  if (type) url += `&type=${type}`;
  
  const response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
}
```

### cURL Examples

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "confirm_email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "login": "john_doe",
    "password": "SecurePass123!"
  }'

# Get Profile
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Get Activity
curl -X GET "http://localhost:5000/api/auth/activity?limit=10&type=single" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🎯 Best Practices

### For Frontend Developers

1. **Store JWT securely**
   - Use `httpOnly` cookies or secure localStorage
   - Never expose tokens in URLs

2. **Validate inputs client-side**
   - Check password strength before submission
   - Validate email format
   - Match confirmation fields

3. **Handle token expiration**
   - Refresh tokens before expiry
   - Redirect to login on 401 errors

4. **Show helpful error messages**
   - Display specific validation errors
   - Guide users to create strong passwords

### For Backend Integration

1. **Log activities automatically**
   ```python
   # After successful download
   auth_service.log_user_activity(username, {
       'activity_type': 'single',
       'download_id': download_id,
       'url': video_url,
       'title': video_title,
       'format': 'mp4',
       'quality': '720p',
       'ip_address': get_client_ip(),
       'status': 'completed',
       'file_size': file_size
   })
   ```

2. **Update activity status**
   ```python
   # When download completes
   auth_service.update_activity_status(
       username,
       download_id,
       'completed',
       completed_at=datetime.utcnow().isoformat(),
       file_size=file_size
   )
   ```

3. **Protect routes**
   ```python
   @app.route('/protected')
   def protected_route():
       token = request.headers.get('Authorization', '').replace('Bearer ', '')
       result = auth_service.verify_token(token)
       if not result.get('valid'):
           return jsonify({'error': 'Unauthorized'}), 401
       # Continue with protected logic
   ```

---

## 🔄 Migration from Old System

If you have existing users without IP tracking:

```python
# Update existing users
for username, user in auth_service.users.items():
    if 'registration_ip' not in user:
        user['registration_ip'] = None
        user['last_login_ip'] = None
        user['last_login_at'] = None
        user['activities'] = []
```

---

## 📈 Statistics & Analytics

Get user statistics:

```python
# Total users
total_users = len(auth_service.users)

# Active users (logged in last 7 days)
from datetime import datetime, timedelta
week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
active_users = sum(
    1 for user in auth_service.users.values()
    if user.get('last_login_at', '') > week_ago
)

# Total downloads
total_downloads = sum(
    len(user.get('activities', []))
    for user in auth_service.users.values()
)
```

---

## 🛡️ Security Considerations

1. **Change default secrets** in production
   - Update `JWT_SECRET_KEY` in `.env`
   - Use strong, random secrets

2. **Enable HTTPS** in production
   - Tokens should only be transmitted over HTTPS
   - Set secure cookie flags

3. **Rate limiting**
   - Implement rate limiting on login endpoint
   - Prevent brute force attacks

4. **Monitor suspicious activity**
   - Track failed login attempts
   - Alert on unusual IP changes
   - Monitor download patterns

---

## 📞 Support

For issues or questions:
- Check the main [README.md](./README.md)
- Review [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- Check [ARCHITECTURE.md](./ARCHITECTURE.md)
