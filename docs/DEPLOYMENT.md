# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Git

### Setup

```bash
# Clone repository
git clone <repo>
cd iam-threat-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with local settings

# Initialize database
python -m alembic upgrade head

# Run development server
python src/main.py
```

Server: http://localhost:8000
API Docs: http://localhost:8000/docs

## Docker Deployment

### Single Container

```bash
# Build image
docker build -t iam-threat-detection:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name iam-threat-app \
  iam-threat-detection:latest
```

### Docker Compose (Recommended for Local)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Reset database
docker-compose down -v
docker-compose up -d
```

Services:
- API: http://localhost:8000
- Database Admin: http://localhost:8080
- PostgreSQL: localhost:5432

## Production Deployment

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iam-threat-detection
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: iam-threat-detection
  template:
    metadata:
      labels:
        app: iam-threat-detection
    spec:
      containers:
      - name: api
        image: iam-threat-detection:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: secret-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Environment Variables

Production (`.env`):
```
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:password@prod-db.aws.rds.amazonaws.com/iam_db
SECRET_KEY=<generate-secure-random-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENABLE_MFA=true
ENABLE_AUDIT_LOGGING=true
```

### Database Setup

```bash
# Create PostgreSQL database
createdb -U postgres iam_threat_db

# Run migrations
alembic upgrade head

# Backup database
pg_dump -U postgres iam_threat_db > backup.sql

# Restore from backup
psql -U postgres -d iam_threat_db < backup.sql
```

## Security Hardening

### 1. Secret Management
```bash
# Use environment variables (never commit secrets)
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# Or use secrets management service
# AWS Secrets Manager, HashiCorp Vault, etc.
```

### 2. HTTPS/TLS
```bash
# Use reverse proxy (Nginx/Apache) for HTTPS
# Generate SSL certificate
certbot certonly --standalone -d yourdomain.com
```

### 3. Database Security
```sql
-- Create restricted user
CREATE USER app_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE iam_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_user;

-- Disable unused extensions
DROP EXTENSION IF EXISTS plpgsql;
```

### 4. CORS Configuration
```python
# In .env
CORS_ORIGINS=["https://yourdomain.com"]
```

### 5. Rate Limiting
```python
# Use FastAPI middleware
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## Monitoring & Logging

### Application Logs
```bash
# View logs
tail -f logs/iam_threat_detection.log

# Rotate logs
logrotate /etc/logrotate.d/iam-threat
```

### Metrics
```bash
# Prometheus metrics endpoint
curl http://localhost:8000/metrics
```

### Alerting
```bash
# Setup monitoring with:
# - Prometheus
# - Grafana
# - AlertManager
```

## Scaling

### Horizontal Scaling
1. Run multiple API instances
2. Use load balancer (nginx, HAProxy, AWS ALB)
3. Share PostgreSQL database across instances

```bash
# Start multiple instances
python -m uvicorn src.main:app --port 8001 &
python -m uvicorn src.main:app --port 8002 &
python -m uvicorn src.main:app --port 8003 &
```

### Database Optimization
```bash
# Connection pooling
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=20

# Add indexes
CREATE INDEX idx_login_attempts_user_id ON login_attempts(user_id);
CREATE INDEX idx_security_alerts_timestamp ON security_alerts(timestamp);
```

## Backup & Recovery

### Automated Backups
```bash
#!/bin/bash
# Daily backup script
BACKUP_DIR="/backups"
DB_NAME="iam_threat_db"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -U postgres $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

### Point-in-time Recovery
```bash
# Enable WAL archiving in postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/wal_archive/%f'
```

## Health Checks

```bash
# Health endpoint
curl http://localhost:8000/health
# Response: {"status": "healthy", "version": "1.0.0"}

# Status endpoint
curl http://localhost:8000/status
# Response: {"app_name": "...", "version": "1.0.0", "features": {...}}
```

## Troubleshooting

### Database Connection Issues
```bash
# Test connection
psql -U postgres -h localhost -d iam_threat_db -c "SELECT 1;"

# Check logs
docker logs iam_threat_app
tail -f logs/iam_threat_detection.log
```

### High Memory Usage
```python
# Check SQLAlchemy pool settings
# Reduce DATABASE_POOL_SIZE if needed
# Enable connection recycling
```

### Slow Queries
```bash
# Enable query logging
set log_min_duration_statement = 1000; -- 1 second

# Check EXPLAIN plans
EXPLAIN ANALYZE SELECT * FROM login_attempts ...;
```

## Maintenance

### Regular Tasks
- Monitor disk usage
- Review audit logs
- Update dependencies
- Rotate secrets
- Test backups
- Performance analysis

### Zero-downtime Deployments
```bash
# Using blue-green deployment
# 1. Deploy new version to green environment
# 2. Run smoke tests
# 3. Switch traffic from blue to green
# 4. Keep blue for rollback
```

