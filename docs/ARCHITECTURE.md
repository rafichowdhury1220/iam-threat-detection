# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
│              (Web, Mobile, Third-party)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────────────────┐
│                     API Gateway / Load Balancer              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                      FastAPI Application                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Routes:                                              │  │
│  │  • Authentication (login, register, MFA)            │  │
│  │  • User Management (CRUD, roles)                    │  │
│  │  • Security (threats, alerts, policies)             │  │
│  │  • Audit Logging (compliance, trails)               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────┬──────────────────────────────┬────────┬────────────┘
         │                              │        │
    ┌────▼─────┐            ┌──────────▼──┐    │
    │   Auth   │            │   Threat    │    │
    │ Service  │            │ Detection   │    │
    │          │            │   Engine    │    │
    └──────────┘            └─────────────┘    │
         │                        │             │
    ┌────▼────────────────────────▼───┐   ┌────▼─────────┐
    │    Persistence Layer             │   │   Logging &  │
    │  • User Repository               │   │  Monitoring  │
    │  • Login Attempt Repository      │   │              │
    │  • Security Alert Repository     │   └──────────────┘
    │  • Audit Log Repository          │
    └────┬──────────────────────────────┘
         │
    ┌────▼──────────────────┐
    │   PostgreSQL Database │
    │                       │
    │  Tables:              │
    │  • users              │
    │  • login_attempts     │
    │  • security_alerts    │
    │  • audit_logs         │
    │  • mfa_backup_codes   │
    │  • security_policies  │
    │  • role_assignments   │
    └──────────────────────┘
```

## Component Architecture

### 1. **API Layer** (`/api`)
- FastAPI route handlers
- Request/response validation
- HTTP error handling
- OpenAPI documentation

### 2. **Authentication & Authorization** (`/auth`)
- JWT token generation and verification
- Password hashing with bcrypt
- Multi-factor authentication (TOTP)
- Role-based access control (RBAC)
- Permission validation

### 3. **Threat Detection Engine** (`/threat_detection`)
- **Impossible Travel Detector**: Uses Haversine formula for geographic distance
- **Failed Login Detector**: Tracks attempts within time windows
- **Privilege Escalation Detector**: Monitors role changes
- Real-time threat analysis

### 4. **Data Models** (`/models`)
- Pydantic schemas for validation
- Type-safe request/response models
- Enumeration types for consistency

### 5. **Persistence Layer** (`/persistence`)
- SQLAlchemy ORM models
- Database connection management
- Transaction handling
- Query optimization

### 6. **Core Services** (`/core`)
- Configuration management
- Environment variable handling
- Structured logging
- Error handling utilities

## Data Flow Examples

### Authentication Flow
```
1. User Login Request
   ├─ Validate credentials
   ├─ Check MFA requirement
   ├─ Generate JWT tokens
   ├─ Record login attempt
   ├─ Run threat detection
   └─ Return tokens

2. Authenticated Request
   ├─ Extract token from header
   ├─ Verify token signature
   ├─ Extract user and role
   ├─ Check permissions
   └─ Process request / Return response
```

### Threat Detection Flow
```
1. Login Attempt Received
   │
   ├─ Extract location & IP
   │  └─ Reverse geocode IP
   │
   ├─ Query previous login
   │  └─ Fetch last location & time
   │
   ├─ Run Threat Detectors
   │  ├─ Impossible Travel Check
   │  │  └─ Calculate distance & required speed
   │  ├─ Failed Login Check
   │  │  └─ Count recent failures
   │  └─ Anomaly Check
   │
   ├─ Generate Alerts
   │  └─ Create SecurityAlert records
   │
   └─ Record Audit Log
      └─ Log all actions taken
```

### Privilege Escalation Flow
```
1. Escalation Request
   │
   ├─ Verify requester authorization
   │
   ├─ Validate target role
   │  └─ Check role hierarchy
   │
   ├─ Trigger threat detection
   │  └─ Privilege escalation detector
   │
   ├─ Enforce MFA (if configured)
   │
   ├─ Create temporary role assignment
   │
   └─ Generate audit trail
```

## Security Architecture

### Authentication Layers
1. **Credentials**: Email + password (bcrypt hashed)
2. **MFA**: TOTP-based (time-based one-time password)
3. **Tokens**: JWT with expiration
4. **Refresh**: Separate refresh tokens with longer TTL

### Authorization Layers
1. **Role-based**: RBAC hierarchy
2. **Permission-based**: Specific action permissions
3. **Resource-based**: Access to specific resources
4. **Temporal**: Time-based access restrictions

### Threat Detection Layers
1. **Real-time**: Immediate threat analysis on login
2. **Behavioral**: Pattern analysis over time
3. **Anomaly**: Detection of unusual activities
4. **Alert**: Graduated response system

## Scalability Considerations

### Database
- Connection pooling (configurable)
- Query optimization with indexes
- Partitioning for large audit logs
- Read replicas for analytics

### Application
- Stateless design (horizontal scaling)
- Async I/O with asyncio
- Background task processing
- Caching for frequently accessed data

### Monitoring
- Structured logging for analysis
- Metrics collection
- Alert thresholds
- Performance monitoring

## Deployment Architecture

### Development
```
Single machine with SQLite or PostgreSQL
All components in one process
Hot reload on code changes
```

### Production
```
Docker containerization
Kubernetes orchestration
PostgreSQL on managed service
Load balancing with health checks
Monitoring and alerting
```

### High Availability
```
Multiple API instances
Database replication
Separate threat detection workers
Message queue for async processing
```

## Integration Points

### External Services
- **Geolocation APIs**: IP-to-location mapping
- **Email Service**: Alert notifications
- **SMS Service**: MFA delivery
- **SIEM Integration**: Security event forwarding
- **LDAP/Active Directory**: External user sync

### Monitoring & Observability
- **Logs**: JSON structured logs
- **Metrics**: Prometheus-formatted metrics
- **Tracing**: OpenTelemetry spans
- **Alerts**: Automated notifications

## Configuration Management

### Environment-based
```
Development → Debug enabled, mock services
Staging → Production config, test data
Production → All security hardened
```

### Feature Flags
```
MFA enforcement
Threat detection levels
Audit logging
Metrics collection
```

