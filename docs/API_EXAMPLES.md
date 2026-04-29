# API Examples

## Authentication Examples

### 1. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "secure_password"
  }'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 2. Setup MFA
```bash
curl -X POST http://localhost:8000/api/v1/auth/mfa/setup \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Response
{
  "secret": "JBSWY3DPEBLW64TMMQ======",
  "qr_code": "data:image/png;base64,...",
  "backup_codes": [
    "XXXXXXXX",
    "YYYYYYYY"
  ]
}
```

### 3. Refresh Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<refresh_token>"
  }'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## User Management Examples

### 1. List Users
```bash
curl -X GET "http://localhost:8000/api/v1/users?skip=0&limit=10" \
  -H "Authorization: Bearer <access_token>"

# Response
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "department": "Engineering",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-20T14:25:00Z"
  }
]
```

### 2. Get User Details
```bash
curl -X GET http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer <access_token>"
```

### 3. Update User
```bash
curl -X PUT http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Smith",
    "department": "Security"
  }'
```

### 4. Assign Role
```bash
curl -X POST http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000/roles/manager \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "duration_hours": 8
  }'

# Response
{
  "status": "success",
  "role": "manager",
  "expires_at": "2024-01-20T16:00:00Z"
}
```

### 5. Get Login History
```bash
curl -X GET "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000/login-history?days=30" \
  -H "Authorization: Bearer <access_token>"

# Response
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "success",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "location": "New York, USA",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timestamp": "2024-01-20T14:25:00Z"
  }
]
```

## Security & Threat Examples

### 1. Get Security Alerts
```bash
curl -X GET "http://localhost:8000/api/v1/security/alerts?severity=high&acknowledged=false" \
  -H "Authorization: Bearer <security_officer_token>"

# Response
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "threat_type": "impossible_travel",
    "threat_level": "high",
    "description": "User traveled 8500km in 45 minutes (required speed: 11333km/h)",
    "location_from": "New York, USA",
    "location_to": "Tokyo, Japan",
    "timestamp": "2024-01-20T14:35:00Z",
    "is_acknowledged": false
  }
]
```

### 2. Request Privilege Escalation
```bash
curl -X POST http://localhost:8000/api/v1/security/users/550e8400-e29b-41d4-a716-446655440000/escalate-privileges \
  -H "Authorization: Bearer <user_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "target_role": "admin",
    "reason": "Incident response investigation",
    "duration_hours": 4
  }'

# Response
{
  "status": "pending_approval",
  "request_id": "550e8400-e29b-41d4-a716-446655440003",
  "message": "Privilege escalation request submitted. Awaiting approval."
}
```

### 3. Acknowledge Alert
```bash
curl -X POST http://localhost:8000/api/v1/security/alerts/550e8400-e29b-41d4-a716-446655440002/acknowledge \
  -H "Authorization: Bearer <security_officer_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "action_taken": "Verified user was traveling. No action needed."
  }'

# Response
{
  "status": "acknowledged",
  "acknowledged_by": "550e8400-e29b-41d4-a716-446655440005",
  "acknowledged_at": "2024-01-20T15:00:00Z"
}
```

### 4. Get Threat Analysis
```bash
curl -X GET "http://localhost:8000/api/v1/security/analysis?period_days=30" \
  -H "Authorization: Bearer <admin_token>"

# Response
{
  "total_threats": 42,
  "threats_by_type": {
    "impossible_travel": 15,
    "multiple_failed_logins": 18,
    "privilege_escalation": 5,
    "unusual_location": 4
  },
  "affected_users": 28,
  "critical_alerts": 3,
  "high_alerts": 12,
  "trends": {
    "daily_average": 1.4,
    "weekly_increase": "5%"
  }
}
```

## Audit Logging Examples

### 1. Get Audit Logs
```bash
curl -X GET "http://localhost:8000/api/v1/audit?resource_type=user&action=update&skip=0&limit=10" \
  -H "Authorization: Bearer <admin_token>"

# Response
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440006",
    "actor_id": "550e8400-e29b-41d4-a716-446655440001",
    "resource_type": "user",
    "resource_id": "550e8400-e29b-41d4-a716-446655440000",
    "action": "update",
    "details": {
      "fields_changed": ["role", "department"]
    },
    "ip_address": "192.168.1.100",
    "status": "success",
    "timestamp": "2024-01-20T15:30:00Z"
  }
]
```

### 2. Get User Audit Trail
```bash
curl -X GET "http://localhost:8000/api/v1/audit/users/550e8400-e29b-41d4-a716-446655440000?days=90" \
  -H "Authorization: Bearer <access_token>"

# Response returns all actions related to the user
```

### 3. Export Audit Logs
```bash
curl -X GET "http://localhost:8000/api/v1/audit/export?start_date=2024-01-01&end_date=2024-01-31&format=json" \
  -H "Authorization: Bearer <admin_token>" \
  > audit_logs.json
```

### 4. Generate Compliance Report
```bash
curl -X GET http://localhost:8000/api/v1/audit/compliance/report?period=monthly \
  -H "Authorization: Bearer <admin_token>"

# Response
{
  "report_period": "2024-01-01 to 2024-01-31",
  "total_users": 150,
  "active_users": 142,
  "new_users": 8,
  "total_login_attempts": 4230,
  "failed_login_attempts": 87,
  "security_alerts": {
    "critical": 2,
    "high": 15,
    "medium": 45,
    "low": 120
  },
  "privilege_changes": 42,
  "mfa_enabled_users": 145,
  "password_changes": 38,
  "deactivated_users": 3
}
```

## Using with Python Requests

```python
import requests
import json

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "username": "user@example.com",
        "password": "password"
    }
)
token = response.json()["access_token"]

# Get alerts with authentication
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/api/v1/security/alerts",
    headers=headers
)
alerts = response.json()
```

