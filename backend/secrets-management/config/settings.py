"""
Configuration Settings

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

Application configuration using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ========================================================================
    # APPLICATION
    # ========================================================================
    APP_NAME: str = "Vaultwarden Secrets Management API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENABLE_DOCS: bool = Field(default=True, env="ENABLE_DOCS")
    
    # ========================================================================
    # API SERVER
    # ========================================================================
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8001, env="API_PORT")
    API_PREFIX: str = Field(default="/api/v1", env="API_PREFIX")
    
    # ========================================================================
    # DATABASE
    # ========================================================================
    DATABASE_URL: str = Field(
        default="postgresql://vaultwarden:password@localhost:5432/vaultwarden",
        env="DATABASE_URL"
    )
    DB_POOL_SIZE: int = Field(default=20, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=40, env="DB_MAX_OVERFLOW")
    DB_ECHO: bool = Field(default=False, env="DB_ECHO")
    
    # ========================================================================
    # SECURITY
    # ========================================================================
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    # Used for signing tokens, generating API keys
    
    API_KEY_LENGTH: int = Field(default=32, env="API_KEY_LENGTH")
    API_KEY_PREFIX: str = Field(default="vw_svc_", env="API_KEY_PREFIX")
    API_KEY_SALT: str = Field(..., env="API_KEY_SALT")
    
    # JWT Settings
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRATION_MINUTES: int = Field(default=60, env="JWT_EXPIRATION_MINUTES")
    
    # Password/Key Hashing
    BCRYPT_ROUNDS: int = Field(default=12, env="BCRYPT_ROUNDS")
    
    # ========================================================================
    # RATE LIMITING
    # ========================================================================
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_PER_SECOND: int = Field(default=100, env="RATE_LIMIT_PER_SECOND")
    RATE_LIMIT_BURST: int = Field(default=200, env="RATE_LIMIT_BURST")
    
    # Redis for rate limiting (optional, can use in-memory)
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    # Example: redis://localhost:6379/0
    
    # ========================================================================
    # CORS
    # ========================================================================
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="ALLOWED_ORIGINS"
    )
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # ========================================================================
    # LOGGING
    # ========================================================================
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    # json or text
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")
    # If set, logs will be written to this file
    
    # ========================================================================
    # ENCRYPTION
    # ========================================================================
    ENCRYPTION_KEY: str = Field(..., env="ENCRYPTION_KEY")
    # 32-byte base64-encoded key for encrypting secrets
    # Generate with: python -c "import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"
    
    # ========================================================================
    # ROTATION
    # ========================================================================
    ROTATION_ENABLED: bool = Field(default=True, env="ROTATION_ENABLED")
    ROTATION_SCHEDULER_INTERVAL: int = Field(default=300, env="ROTATION_SCHEDULER_INTERVAL")
    # Check for due rotations every N seconds (default: 5 minutes)
    
    # ========================================================================
    # INTEGRATIONS
    # ========================================================================
    
    # Vaultwarden Integration
    VAULTWARDEN_URL: str = Field(
        default="http://localhost:80",
        env="VAULTWARDEN_URL"
    )
    VAULTWARDEN_ADMIN_TOKEN: Optional[str] = Field(
        default=None,
        env="VAULTWARDEN_ADMIN_TOKEN"
    )
    
    # GitHub Actions
    GITHUB_APP_ID: Optional[str] = Field(default=None, env="GITHUB_APP_ID")
    GITHUB_PRIVATE_KEY: Optional[str] = Field(default=None, env="GITHUB_PRIVATE_KEY")
    
    # GitLab CI
    GITLAB_URL: Optional[str] = Field(default=None, env="GITLAB_URL")
    GITLAB_TOKEN: Optional[str] = Field(default=None, env="GITLAB_TOKEN")
    
    # Kubernetes
    K8S_IN_CLUSTER: bool = Field(default=False, env="K8S_IN_CLUSTER")
    K8S_CONFIG_FILE: Optional[str] = Field(default=None, env="K8S_CONFIG_FILE")
    
    # ========================================================================
    # MONITORING
    # ========================================================================
    METRICS_ENABLED: bool = Field(default=True, env="METRICS_ENABLED")
    PROMETHEUS_PORT: int = Field(default=9090, env="PROMETHEUS_PORT")
    
    # ========================================================================
    # AUDIT
    # ========================================================================
    AUDIT_LOG_RETENTION_DAYS: int = Field(default=365, env="AUDIT_LOG_RETENTION_DAYS")
    # How long to keep audit logs
    
    # ========================================================================
    # FEATURES FLAGS
    # ========================================================================
    FEATURE_SECRET_VERSIONING: bool = Field(default=True, env="FEATURE_SECRET_VERSIONING")
    FEATURE_AUTOMATIC_ROTATION: bool = Field(default=True, env="FEATURE_AUTOMATIC_ROTATION")
    FEATURE_DYNAMIC_SECRETS: bool = Field(default=False, env="FEATURE_DYNAMIC_SECRETS")
    # Not implemented in Phase 1
    
    # ========================================================================
    # CONFIGURATION
    # ========================================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # ========================================================================
    # COMPUTED PROPERTIES
    # ========================================================================
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def database_config(self) -> dict:
        """Get database configuration for SQLAlchemy"""
        return {
            "url": self.DATABASE_URL,
            "pool_size": self.DB_POOL_SIZE,
            "max_overflow": self.DB_MAX_OVERFLOW,
            "echo": self.DB_ECHO,
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    
    Returns:
        Settings: Application settings
    """
    return Settings()


# Export settings instance
settings = get_settings()

