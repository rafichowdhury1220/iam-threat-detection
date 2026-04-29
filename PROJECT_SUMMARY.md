# Project Summary & Quick Reference

## About This Project

This is a **production-grade Identity and Access Management (IAM) Threat Detection System** built in Python with FastAPI. It demonstrates:

### IAM Engineer Skills
- ✅ Multi-factor authentication (TOTP-based)
- ✅ Role-based access control (RBAC) with hierarchies
- ✅ JWT token management with refresh capabilities
- ✅ Secure password management (bcrypt hashing)
- ✅ Comprehensive audit logging for compliance
- ✅ Privilege escalation management

### Solution Architect Skills
- ✅ Scalable system design (async-first)
- ✅ Layered architecture (API, service, persistence)
- ✅ Database design with proper indexing
- ✅ Real-time threat detection engine
- ✅ Configuration management
- ✅ Monitoring and observability
- ✅ Deployment strategy (Docker, Kubernetes)
- ✅ Security hardening
- ✅ Performance optimization
- ✅ Testing strategy (unit, integration)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.104 |
| Runtime | Python 3.11+ |
| Database | PostgreSQL 13+ |
| Authentication | JWT (python-jose) |
| Password Security | Passlib + bcrypt |
| MFA | PyOTP (TOTP) |
| ORM | SQLAlchemy 2.0 |
| Logging | Structlog (JSON) |
| Testing | Pytest |
| Container | Docker + Docker Compose |
| Code Quality | Black, isort, flake8, mypy |

## Key Features

### Threat Detection
1. **Impossible Travel Detection**
   - Calculates geographic distance using Haversine formula
   - Detects travel speeds exceeding physical possibility
   - Customizable thresholds

2. **Failed Login Detection**
   - Tracks failed attempts per user/IP
   - Time-window based analysis
   - Automatic account lockout
   - Progressive delays

3. **Privilege Escalation Monitoring**
   - Tracks role changes
   - Alerts on unauthorized escalations
   - Enforces MFA for sensitive escalations

### Enterprise Features
- Real-time security alerts with severity levels
- Comprehensive audit logging (all actions tracked)
- Compliance reporting
- Security policies configuration
- User account lifecycle management
- Temporary role assignments with expiration

## Quick Start

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with database credentials

# 3. Initialize Database
python -m alembic upgrade head

# 4. Run
python src/main.py

# 5. Access
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## Project Structure

```
iam-threat-detection/
├── src/
│   ├── main.py                          # FastAPI app
│   ├── dev.py                           # Dev server
│   └── iam_threat_detection/
│       ├── auth/                        # Authentication & RBAC
│       ├── threat_detection/            # Threat detection engine
│       ├── api/                         # REST endpoints
│       ├── models/                      # Data schemas
│       ├── persistence/                 # Database layer
│       └── core/                        # Config & logging
├── tests/                               # Unit & integration tests
├── docs/                                # Documentation
│   ├── ARCHITECTURE.md                  # System design
│   ├── API_EXAMPLES.md                  # API usage
│   ├── DATABASE_SCHEMA.md               # Data model
│   ├── DEPLOYMENT.md                    # Deployment guide
│   └── SECURITY.md                      # Security guidelines
├── pyproject.toml                       # Project metadata
├── requirements.txt                     # Dependencies
├── Dockerfile                           # Container image
├── docker-compose.yml                   # Local development
├── .env.example                         # Configuration template
└── README.md                            # Full documentation
```

## Core Modules

### Authentication (`auth/`)
- `AuthService`: Token generation, verification, password hashing
- `RBACService`: Role hierarchy, permission management
- `MFAService`: TOTP generation, backup codes

### Threat Detection (`threat_detection/`)
- `ImpossibleTravelDetector`: Geographic anomalies
- `FailedLoginDetector`: Brute force detection
- `PrivilegeEscalationDetector`: Role escalation monitoring
- `ThreatDetectionEngine`: Orchestrator

### API Routes (`api/`)
- `auth.py`: Login, register, MFA, tokens
- `users.py`: User CRUD, role assignment
- `security.py`: Threats, alerts, policies
- `audit.py`: Compliance, logs, reports

## Example Usage

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user@example.com", "password": "password"}'
```

### Get Security Alerts
```bash
curl -X GET "http://localhost:8000/api/v1/security/alerts?severity=high" \
  -H "Authorization: Bearer <token>"
```

### Assign Role
```bash
curl -X POST http://localhost:8000/api/v1/users/{user_id}/roles/manager \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"duration_hours": 4}'
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/auth/login` | User login |
| POST | `/api/v1/auth/mfa/setup` | Setup MFA |
| POST | `/api/v1/auth/refresh` | Refresh token |
| GET | `/api/v1/users` | List users (admin) |
| PUT | `/api/v1/users/{id}` | Update user |
| GET | `/api/v1/security/alerts` | Get alerts |
| POST | `/api/v1/security/alerts/{id}/acknowledge` | Acknowledge alert |
| GET | `/api/v1/audit` | Get audit logs |
| GET | `/api/v1/audit/compliance/report` | Compliance report |

## Security Highlights

- **Passwords**: Bcrypt hashing (12 rounds)
- **Tokens**: HS256 JWT with configurable expiration
- **MFA**: TOTP-based with backup codes
- **Audit**: All actions logged with timestamp, actor, and details
- **RBAC**: Hierarchical roles with permission checking
- **Rate Limiting**: Brute force protection
- **HTTPS**: Required in production
- **Secrets**: Managed via environment variables

## Database Schema

### Core Tables
- `users`: User accounts and properties
- `login_attempts`: Login events for threat analysis
- `security_alerts`: Detected threats and alerts
- `audit_logs`: Comprehensive action trail
- `mfa_backup_codes`: MFA recovery codes
- `security_policies`: Configurable policies
- `role_assignments`: Role tracking including temporary escalations

## Testing

```bash
# All tests
pytest

# With coverage
pytest --cov=src/iam_threat_detection

# Specific test file
pytest tests/test_auth.py -v

# Watch mode
pytest-watch
```

## Development Commands

```bash
# Code formatting
black src/ tests/
isort src/ tests/

# Linting
flake8 src/
mypy src/

# Type checking
mypy src/ --strict

# Database migrations
alembic revision --autogenerate -m "add table"
alembic upgrade head
alembic downgrade -1

# Docker
docker-compose up      # Start
docker-compose down    # Stop
docker-compose logs -f # Logs
```

## Configuration

Key environment variables in `.env`:

```
# Security
SECRET_KEY=<secure-random-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://user:pass@localhost/db
DATABASE_POOL_SIZE=20

# Threat Detection
IMPOSSIBLE_TRAVEL_THRESHOLD_KM=1000
FAILED_LOGIN_THRESHOLD=5
FAILED_LOGIN_WINDOW_MINUTES=15

# Features
ENABLE_MFA=true
ENABLE_AUDIT_LOGGING=true
ENABLE_THREAT_DETECTION=true
```

## Deployment

### Development
```bash
python src/main.py
```

### Docker
```bash
docker build -t iam-threat-detection .
docker run -p 8000:8000 --env-file .env iam-threat-detection
```

### Docker Compose
```bash
docker-compose up -d
```

### Kubernetes
See `docs/DEPLOYMENT.md` for Kubernetes manifests

## Monitoring

- **Health**: GET `/health`
- **Status**: GET `/status`
- **Logs**: Structured JSON logs to `logs/iam_threat_detection.log`
- **Metrics**: Prometheus-format metrics at `/metrics`

## Documentation

- **README.md**: Full project overview
- **docs/ARCHITECTURE.md**: System design and data flow
- **docs/API_EXAMPLES.md**: cURL and Python examples
- **docs/DATABASE_SCHEMA.md**: Table definitions
- **docs/DEPLOYMENT.md**: Production deployment
- **docs/SECURITY.md**: Security guidelines

## Support & Resources

- API Documentation: http://localhost:8000/docs (Swagger UI)
- Architecture: See docs/ARCHITECTURE.md
- Security: See docs/SECURITY.md
- Deployment: See docs/DEPLOYMENT.md
- Contributing: See CONTRIBUTING.md

## License

MIT License - See LICENSE for details

---

**Built to demonstrate comprehensive IAM engineering and enterprise architecture capabilities**
