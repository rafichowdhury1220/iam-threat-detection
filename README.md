# IAM Threat Detection System

## Overview

An enterprise-grade **Identity and Access Management (IAM) Threat Detection System** built with FastAPI, demonstrating advanced capabilities in:

- **IAM Engineering**: Multi-factor authentication, role-based access control, privilege management, and comprehensive audit logging
- **Solution Architecture**: Scalable design patterns, threat detection engine, security policies, and monitoring infrastructure

## Key Features

### Security & Authentication
- ✅ JWT-based token authentication with refresh capabilities
- ✅ Multi-Factor Authentication (MFA) with TOTP support
- ✅ Role-Based Access Control (RBAC) with hierarchical permissions
- ✅ Secure password hashing with bcrypt
- ✅ Token expiration and refresh mechanisms

### Threat Detection Engine
- ✅ **Impossible Travel Detection**: Detects geographic impossibilities using Haversine formula
- ✅ **Failed Login Analysis**: Tracks and alerts on multiple failed login attempts
- ✅ **Privilege Escalation Monitoring**: Alerts on unauthorized role escalations
- ✅ **Location & Time Anomalies**: Identifies unusual access patterns
- ✅ **Real-time Analysis**: Instant threat notifications

### Enterprise Features
- ✅ Comprehensive Audit Logging: All system actions tracked with actor, resource, and timestamp
- ✅ Security Alerts & Notifications: Multi-level threat severity system
- ✅ User & Account Management: Complete lifecycle management
- ✅ Security Policies: Configurable threat detection rules
- ✅ Compliance Reporting: Audit trails and activity analysis

### Architecture
- ✅ Async-first design with FastAPI
- ✅ SQLAlchemy ORM with PostgreSQL support
- ✅ Structured logging with JSON output
- ✅ Modular service-oriented architecture
- ✅ Production-ready configuration management

## Project Structure

```
iam-threat-detection/
├── src/
│   ├── main.py                      # FastAPI application entry point
│   ├── dev.py                       # Development server
│   └── iam_threat_detection/
│       ├── __init__.py
│       ├── core/                    # Configuration and utilities
│       │   ├── config.py            # Settings management
│       │   └── logger.py            # Structured logging
│       ├── auth/                    # Authentication & authorization
│       │   └── __init__.py          # Auth services, RBAC, MFA
│       ├── threat_detection/        # Threat detection engine
│       │   └── __init__.py          # Impossible travel, failed logins, etc.
│       ├── models/                  # Data schemas & Pydantic models
│       │   └── __init__.py
│       ├── api/                     # REST API endpoints
│       │   ├── auth.py              # Authentication routes
│       │   ├── users.py             # User management
│       │   ├── security.py          # Security & alerts
│       │   └── audit.py             # Audit logging
│       └── persistence/             # Database layer
│           ├── database.py          # SQLAlchemy setup
│           └── models.py            # Database models
├── tests/                           # Unit and integration tests
├── config/                          # Configuration files
├── docs/                            # Documentation
├── pyproject.toml                   # Project configuration
├── .env.example                     # Environment variables template
├── requirements.txt                 # Python dependencies
└── Dockerfile                       # Container image
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- pip or conda

### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd iam-threat-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
python -m alembic upgrade head

# Start development server
python src/main.py
```

Server runs at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - New user registration
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/mfa/setup` - Setup MFA
- `POST /api/v1/auth/mfa/verify` - Verify MFA code

### Users
- `GET /api/v1/users` - List users (admin)
- `GET /api/v1/users/{user_id}` - Get user details
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user
- `GET /api/v1/users/{user_id}/login-history` - Login history
- `POST /api/v1/users/{user_id}/roles/{role}` - Assign role
- `DELETE /api/v1/users/{user_id}/roles/{role}` - Revoke role

### Security
- `GET /api/v1/security/alerts` - Get security alerts
- `GET /api/v1/security/alerts/{alert_id}` - Alert details
- `POST /api/v1/security/alerts/{alert_id}/acknowledge` - Acknowledge alert
- `GET /api/v1/security/users/{user_id}/threats` - User threats
- `POST /api/v1/security/users/{user_id}/escalate-privileges` - Request escalation
- `GET /api/v1/security/policies` - Get policies
- `GET /api/v1/security/analysis` - Threat analysis

### Audit Logs
- `GET /api/v1/audit` - Get audit logs
- `GET /api/v1/audit/users/{user_id}` - User audit trail
- `GET /api/v1/audit/resources/{type}/{id}` - Resource audit trail
- `GET /api/v1/audit/export` - Export audit logs
- `GET /api/v1/audit/compliance/report` - Compliance report

## Configuration

All settings are managed through environment variables in `.env`:

- **Database**: PostgreSQL connection string and pool settings
- **Security**: JWT secret, algorithm, token expiration
- **MFA**: Multi-factor authentication settings
- **Threat Detection**: Thresholds for impossible travel, failed logins
- **Logging**: Log level, format, and file location
- **Features**: Toggle security features on/off

## Technologies

- **Framework**: FastAPI (high-performance async Python web framework)
- **ORM**: SQLAlchemy 2.0 (database abstraction)
- **Database**: PostgreSQL (production-ready RDBMS)
- **Authentication**: Python-Jose (JWT handling)
- **Password Security**: Passlib with bcrypt (secure hashing)
- **Logging**: Structlog (structured JSON logging)
- **Testing**: Pytest (unit and integration tests)

## Security Considerations

1. **Secret Management**: Use environment variables, never commit secrets
2. **HTTPS**: Always use HTTPS in production
3. **Database**: Use strong credentials, restrict access
4. **MFA**: Enforce MFA for privileged accounts
5. **Rate Limiting**: Implement rate limiting for login endpoints
6. **CORS**: Configure CORS appropriately for your domain
7. **Audit Logging**: Enable comprehensive audit logging
8. **Monitoring**: Monitor threats and alerts in real-time

## Testing

```bash
# Run tests with coverage
pytest --cov=src/iam_threat_detection

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Development

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/

# Pre-commit checks
pre-commit run --all-files
```

## Deployment

See [Docker setup](#docker) or deployment guide for production deployment instructions.

### Docker

```bash
# Build image
docker build -t iam-threat-detection:latest .

# Run container
docker run -p 8000:8000 --env-file .env iam-threat-detection:latest
```

## Architecture Highlights

### Threat Detection Engine
Real-time analysis of login patterns:
- **Haversine Formula** for distance calculation
- **Time window analysis** for travel feasibility
- **Failed login tracking** with configurable thresholds
- **Privilege escalation monitoring** with role hierarchy

### RBAC System
Hierarchical role management:
- Admin (100) → Security Officer (80) → Manager (50) → User (20) → Guest (10)
- Permission-based access control
- Role escalation with audit trails

### Security Pipeline
```
Login Request
    ↓
[ Credential Validation ]
    ↓
[ MFA Verification ]
    ↓
[ Threat Analysis ]
    ├─ Impossible Travel Detection
    ├─ Failed Login Detection
    └─ Location Anomalies
    ↓
[ Access Grant/Deny ]
    ↓
[ Audit Logging ]
```

## Contributing

1. Follow PEP 8 style guidelines
2. Use type hints throughout
3. Write tests for new features
4. Update documentation
5. Create pull requests with clear descriptions

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please:
1. Check existing issues
2. Review documentation
3. Create detailed issue reports
4. Submit pull requests

---

**Built as a demonstration of IAM Engineering and Solution Architecture capabilities**
