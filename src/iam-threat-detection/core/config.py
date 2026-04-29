"""Application configuration and environment management"""

import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "IAM Threat Detection System"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"

    # API Configuration
    api_title: str = "IAM Threat Detection API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/iam_threat_db"
    database_pool_size: int = 20
    database_max_overflow: int = 20
    database_echo: bool = False

    # Security
    secret_key: str = "your-secret-key-change-in-prod"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # JWT
    jwt_audience: str = "iam-threat-detection"
    jwt_issuer: str = "iam-threat-detection"

    # CORS
    cors_origins: List[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]

    # Threat Detection
    impossible_travel_threshold_km: float = 1000.0  # km per minute
    impossible_travel_time_threshold_minutes: int = 15
    failed_login_threshold: int = 5  # Max failed attempts in 15 minutes
    failed_login_window_minutes: int = 15
    privilege_escalation_alert: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "logs/iam_threat_detection.log"

    # Features
    enable_mfa: bool = True
    enable_audit_logging: bool = True
    enable_threat_detection: bool = True
    enable_metrics: bool = True

    # GeoIP (optional)
    geoip_database_path: str = "/opt/geoip/GeoLite2-City.mmdb"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Load settings from environment
settings = Settings()
