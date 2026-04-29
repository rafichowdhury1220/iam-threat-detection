"""Database models using SQLAlchemy ORM"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Float, ForeignKey, 
    Integer, String, Text, ARRAY, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """User entity"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(255), nullable=True)
    role = Column(String(50), default="user", index=True)
    is_active = Column(Boolean, default=True, index=True)
    is_mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    last_ip_address = Column(String(45), nullable=True)
    last_location = Column(String(255), nullable=True)

    # Relationships
    login_attempts = relationship("LoginAttempt", back_populates="user")
    security_alerts = relationship("SecurityAlert", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="actor")
    mfa_backup_codes = relationship("MFABackupCode", back_populates="user")


class LoginAttempt(Base):
    """Track login attempts for threat detection"""
    __tablename__ = "login_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    status = Column(String(50), index=True)  # success, failed, blocked, mfa_pending
    ip_address = Column(String(45), index=True)
    user_agent = Column(Text)
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="login_attempts")


class SecurityAlert(Base):
    """Security threat alerts"""
    __tablename__ = "security_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    threat_type = Column(String(100), index=True)  # impossible_travel, etc.
    threat_level = Column(String(20), index=True)  # critical, high, medium, low
    description = Column(Text)
    location_from = Column(String(255))
    location_to = Column(String(255))
    coordinates_from = Column(ARRAY(Float))  # [latitude, longitude]
    coordinates_to = Column(ARRAY(Float))
    time_difference_minutes = Column(Integer)
    is_acknowledged = Column(Boolean, default=False, index=True)
    acknowledged_by = Column(UUID(as_uuid=True), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    action_taken = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="security_alerts")


class AuditLog(Base):
    """Comprehensive audit trail"""
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resource_type = Column(String(100), index=True)  # user, policy, role, etc.
    resource_id = Column(UUID(as_uuid=True), index=True)
    action = Column(String(100), index=True)  # create, update, delete
    details = Column(JSON)  # Additional action details
    ip_address = Column(String(45))
    status = Column(String(50))  # success, failure
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    actor = relationship("User", back_populates="audit_logs")


class MFABackupCode(Base):
    """Backup codes for MFA"""
    __tablename__ = "mfa_backup_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    code_hash = Column(String(255), unique=True)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="mfa_backup_codes")


class SecurityPolicy(Base):
    """Security policies and configurations"""
    __tablename__ = "security_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text)
    policy_type = Column(String(100))  # mfa, password, access, etc.
    rules = Column(JSON)  # Policy rules/config
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), nullable=True)


class RoleAssignment(Base):
    """Track role assignments and escalations"""
    __tablename__ = "role_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    role = Column(String(50), index=True)
    assigned_by = Column(UUID(as_uuid=True), nullable=True)
    is_temporary = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)
    reason = Column(Text)
    assigned_at = Column(DateTime, default=datetime.utcnow, index=True)
