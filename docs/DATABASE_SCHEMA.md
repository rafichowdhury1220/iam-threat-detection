# Database Schema

## Overview

The IAM system uses PostgreSQL with the following core tables:

## Tables

### users
Primary user accounts table.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_mfa_enabled BOOLEAN NOT NULL DEFAULT false,
    mfa_secret VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login TIMESTAMP,
    last_ip_address VARCHAR(45),
    last_location VARCHAR(255)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);
```

### login_attempts
Tracks all login events for threat detection.

```sql
CREATE TABLE login_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(50) NOT NULL,  -- success, failed, blocked, mfa_pending
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    location VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_login_attempts_user_id ON login_attempts(user_id);
CREATE INDEX idx_login_attempts_ip_address ON login_attempts(ip_address);
CREATE INDEX idx_login_attempts_timestamp ON login_attempts(timestamp);
CREATE INDEX idx_login_attempts_status ON login_attempts(status);
```

### security_alerts
Threat detection alerts and notifications.

```sql
CREATE TABLE security_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    threat_type VARCHAR(100) NOT NULL,  -- impossible_travel, failed_logins, etc.
    threat_level VARCHAR(20) NOT NULL,  -- critical, high, medium, low
    description TEXT NOT NULL,
    location_from VARCHAR(255),
    location_to VARCHAR(255),
    coordinates_from FLOAT[],  -- [latitude, longitude]
    coordinates_to FLOAT[],
    time_difference_minutes INTEGER,
    is_acknowledged BOOLEAN NOT NULL DEFAULT false,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP,
    action_taken VARCHAR(255),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_security_alerts_user_id ON security_alerts(user_id);
CREATE INDEX idx_security_alerts_threat_type ON security_alerts(threat_type);
CREATE INDEX idx_security_alerts_threat_level ON security_alerts(threat_level);
CREATE INDEX idx_security_alerts_timestamp ON security_alerts(timestamp);
CREATE INDEX idx_security_alerts_acknowledged ON security_alerts(is_acknowledged);
```

### audit_logs
Comprehensive audit trail of all system actions.

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id UUID REFERENCES users(id),
    resource_type VARCHAR(100) NOT NULL,  -- user, policy, role, etc.
    resource_id UUID NOT NULL,
    action VARCHAR(100) NOT NULL,  -- create, update, delete
    details JSONB,  -- Additional action details
    ip_address VARCHAR(45),
    status VARCHAR(50) NOT NULL,  -- success, failure
    error_message TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_actor_id ON audit_logs(actor_id);
CREATE INDEX idx_audit_logs_resource_type ON audit_logs(resource_type);
CREATE INDEX idx_audit_logs_resource_id ON audit_logs(resource_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
```

### mfa_backup_codes
Backup codes for multi-factor authentication recovery.

```sql
CREATE TABLE mfa_backup_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    code_hash VARCHAR(255) UNIQUE NOT NULL,
    is_used BOOLEAN NOT NULL DEFAULT false,
    used_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_mfa_backup_codes_user_id ON mfa_backup_codes(user_id);
```

### security_policies
Configurable security policies and rules.

```sql
CREATE TABLE security_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    policy_type VARCHAR(100),  -- mfa, password, access, etc.
    rules JSONB,  -- Policy configuration
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_security_policies_name ON security_policies(name);
CREATE INDEX idx_security_policies_is_active ON security_policies(is_active);
```

### role_assignments
Track role assignments including temporary escalations.

```sql
CREATE TABLE role_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    role VARCHAR(50) NOT NULL,
    assigned_by UUID REFERENCES users(id),
    is_temporary BOOLEAN NOT NULL DEFAULT false,
    expires_at TIMESTAMP,
    reason TEXT,
    assigned_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_role_assignments_user_id ON role_assignments(user_id);
CREATE INDEX idx_role_assignments_expires_at ON role_assignments(expires_at);
```

## Relationships

```
users (1) ──── (n) login_attempts
users (1) ──── (n) security_alerts
users (1) ──── (n) mfa_backup_codes
users (1) ──── (n) role_assignments
users (1) ──── (n) audit_logs (as actor)
security_alerts (n) ──── (1) users (acknowledged_by)
```

## Key Design Decisions

### UUIDs for Primary Keys
- Distributed system friendly
- Better security (not guessable)
- Supports global identifiers

### JSONB for Details
- Flexible schema for audit logs
- Queryable and indexable
- PostgreSQL native

### Timestamps
- All records have `created_at`
- Update operations have `updated_at`
- All in UTC (ISO 8601 format)
- Indexed for range queries

### Indexing Strategy
- Foreign keys indexed (for joins)
- Frequently queried columns indexed
- Timestamp columns indexed (range queries)
- Composite indexes for common filters

## Query Examples

### Get user's recent logins
```sql
SELECT * FROM login_attempts 
WHERE user_id = $1 
  AND timestamp > NOW() - INTERVAL '30 days'
ORDER BY timestamp DESC;
```

### Get unacknowledged alerts
```sql
SELECT * FROM security_alerts
WHERE is_acknowledged = false
  AND threat_level IN ('critical', 'high')
ORDER BY timestamp DESC;
```

### Audit trail for specific user
```sql
SELECT * FROM audit_logs
WHERE actor_id = $1 OR resource_id = $1
ORDER BY timestamp DESC
LIMIT 100;
```

### Login attempts in time window
```sql
SELECT user_id, COUNT(*) as attempts
FROM login_attempts
WHERE status = 'failed'
  AND timestamp > NOW() - INTERVAL '15 minutes'
GROUP BY user_id
HAVING COUNT(*) >= 5;
```

## Maintenance

### Regular Backups
```bash
pg_dump iam_threat_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Archive Old Logs
```sql
-- Move audit logs older than 1 year to archive
INSERT INTO audit_logs_archive 
SELECT * FROM audit_logs 
WHERE timestamp < NOW() - INTERVAL '1 year';

DELETE FROM audit_logs 
WHERE timestamp < NOW() - INTERVAL '1 year';
```

### Analyze for Query Optimization
```sql
ANALYZE users;
ANALYZE login_attempts;
ANALYZE security_alerts;
VACUUM ANALYZE;
```

### Reindex
```sql
REINDEX INDEX idx_login_attempts_user_id;
REINDEX TABLE login_attempts;
```

