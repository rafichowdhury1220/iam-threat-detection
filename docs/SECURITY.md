# Security Guidelines

## Core Principles

1. **Confidentiality**: Data is encrypted and protected
2. **Integrity**: Data cannot be modified without detection
3. **Availability**: Systems are reliable and accessible
4. **Accountability**: All actions are audited and traceable

## Authentication Security

### Password Policy
- Minimum 8 characters
- Mix of upper/lower case, numbers, special characters
- No dictionary words
- Password expiration: 90 days
- History: Don't allow last 5 passwords
- Lockout: 5 failed attempts → 15 minute lockout

### JWT Security
- Algorithm: HS256 (HMAC with SHA-256)
- Secret Key: Generated from `secrets.token_urlsafe(32)`
- Token Expiration: 30 minutes (access) / 7 days (refresh)
- Audience/Issuer: Validated on each request
- Never store tokens in localStorage (use httpOnly cookies)

### MFA Implementation
- TOTP (Time-based One-Time Password)
- 6-digit codes, 30-second window
- Backup codes for account recovery
- MFA mandatory for privileged roles

## Authorization Security

### Role Hierarchy
```
Admin (100)
  ├─ All permissions
  └─ Can manage all users and policies

Security Officer (80)
  ├─ View/acknowledge alerts
  ├─ Enforce MFA
  └─ View audit logs

Manager (50)
  ├─ View user information
  └─ View department alerts

User (20)
  ├─ Self-service options only
  └─ View own records

Guest (10)
  └─ Public endpoints only
```

### Permission Enforcement
- Check permissions on every endpoint
- Default deny (whitelist approach)
- Cache permission results (with timeout)
- Log permission denials

## Data Protection

### Encryption at Rest
```python
# Database passwords encrypted
# Sensitive fields in database should be encrypted
# Use pg_crypto or similar

# Backup encryption
gpg --encrypt backup.sql
```

### Encryption in Transit
- HTTPS/TLS required
- Minimum TLS 1.2
- Forward secrecy enabled
- HSTS headers

### Data Minimization
- Only collect necessary data
- Retention policies
- Automatic purge of old logs
- Anonymize test data

## Audit Logging

### What to Log
✓ All authentication attempts (success/failure)
✓ All authorization decisions
✓ All data modifications
✓ All privileged operations
✓ All security alerts
✗ Don't log passwords
✗ Don't log MFA codes
✗ Don't log PII unnecessarily

### Log Format
```json
{
  "timestamp": "2024-01-20T15:30:00Z",
  "event_type": "authentication",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "login",
  "status": "success",
  "ip_address": "192.168.1.100",
  "details": {
    "mfa_required": true,
    "mfa_verified": true
  }
}
```

### Log Security
- Immutable logs (append-only)
- Signed with digital signature
- Stored separately from application
- Limited read access (audit team only)
- Integrated monitoring tools

## Threat Detection

### Impossible Travel
- Distance calculation using Haversine formula
- Default threshold: 1000 km/minute
- Customizable based on use case

### Failed Login Detection
- Tracks failed attempts per user/IP
- Lockout after 5 attempts in 15 minutes
- Progressive delays between attempts

### Account Lockout
```
Attempt 1-4: Allow retry
Attempt 5:   Lock for 15 minutes
Attempt 10:  Lock for 1 hour
Attempt 20:  Escalate to security team
```

## API Security

### Input Validation
- Validate all inputs with Pydantic
- String length limits
- Numeric ranges
- Email format validation
- UUID validation

### Rate Limiting
```python
# Example with slowapi
@limiter.limit("10/minute")
async def login(credentials):
    ...
```

### CORS Configuration
```python
# Production configuration
CORS_ORIGINS = ["https://yourdomain.com"]
CORS_CREDENTIALS = True  # Allow cookies
CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
```

### SQL Injection Prevention
- Use parameterized queries (SQLAlchemy)
- Never concatenate user input
- Validate input types

## Database Security

### Access Control
```sql
-- Principle of least privilege
CREATE USER app_user WITH PASSWORD 'strong_pass';
GRANT CONNECT ON DATABASE iam_db TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.* TO app_user;
REVOKE DELETE ON public.users FROM app_user; -- No delete on users
```

### Encryption
```sql
-- Sensitive columns encrypted
ALTER TABLE users ADD COLUMN ssn_encrypted bytea;
-- Use pgcrypto extension
UPDATE users SET ssn_encrypted = pgp_sym_encrypt(ssn, 'encryption_key');
```

### Backups
```bash
# Encrypted backups
pg_dump iam_db | gzip | gpg --encrypt > backup.sql.gz.gpg

# Stored securely
# - Separate location from production
# - Limited access
# - Tested regularly
```

## Infrastructure Security

### Network
- Firewall rules (allow only necessary ports)
- IP whitelisting for admin access
- VPN for remote connections
- DDoS protection

### Host Security
- Minimal software installation
- Regular security updates
- SELinux/AppArmor enabled
- Log aggregation

### Container Security
```dockerfile
# Non-root user
RUN useradd -m appuser
USER appuser

# Read-only filesystem (where possible)
ENV PYTHONUNBUFFERED=1

# No secrets in image
# Use secret management
```

## Compliance

### Standards Compliance
- OWASP Web Application Security Testing Guide
- NIST Cybersecurity Framework
- PCI DSS (if handling payments)
- GDPR (if handling EU data)
- SOC 2 Type II (if required)

### Regular Audits
- Annual security audit
- Penetration testing
- Code reviews
- Dependency scanning

## Incident Response

### Security Incident Notification
```
Detection → Assessment → Containment → 
  Eradication → Recovery → Post-Incident
```

### Escalation Path
1. Security team alerts (threshold-based)
2. Team lead review
3. Management notification (if serious)
4. External notification (if required by law)

### Incident Logging
- Document all steps taken
- Timeline of events
- Root cause analysis
- Preventive measures

## Developer Security

### Code Review Checklist
- ✓ No hardcoded secrets
- ✓ Input validation
- ✓ SQL injection prevention
- ✓ XSS prevention
- ✓ CSRF tokens
- ✓ Proper error handling
- ✓ Logging of security events

### Dependency Management
```bash
# Regular scanning
pip install safety
safety check

# Update regularly
pip install --upgrade pip
pip install -U -r requirements.txt
```

### Git Security
```bash
# Use SSH keys for authentication
# Protect main branch
# Require code review before merge
# Sign commits
git config --global user.signingKey <key-id>
git commit -S -m "message"
```

## Security Checklist

- [ ] All inputs validated
- [ ] All outputs encoded
- [ ] Authentication mechanisms in place
- [ ] Authorization enforced
- [ ] Audit logging enabled
- [ ] Threat detection active
- [ ] Encryption at rest and in transit
- [ ] HTTPS only
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Dependencies up to date
- [ ] Secrets in environment variables
- [ ] Backups tested
- [ ] Incident response plan in place
- [ ] Security training complete
