"""
Database Models

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

SQLAlchemy ORM models for secrets management
"""

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Text, 
    ForeignKey, Index, ARRAY, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET, BYTEA
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import text
from datetime import datetime
from uuid import uuid4

Base = declarative_base()


# ============================================================================
# SERVICE ACCOUNTS
# ============================================================================

class ServiceAccount(Base):
    """Service account model"""
    
    __tablename__ = "service_accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    permissions = Column(JSONB, nullable=False, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(255), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    active = Column(Boolean, default=True, nullable=False, index=True)
    metadata = Column(JSONB, default={})
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="service_account", cascade="all, delete-orphan")
    audit_logs = relationship("SecretAuditLog", back_populates="service_account")
    
    # Indexes
    __table_args__ = (
        Index('idx_service_accounts_name', 'name'),
        Index('idx_service_accounts_active', 'active'),
        Index('idx_service_accounts_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<ServiceAccount(id={self.id}, name={self.name}, active={self.active})>"


# ============================================================================
# API KEYS
# ============================================================================

class APIKey(Base):
    """API key model"""
    
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_account_id = Column(UUID(as_uuid=True), ForeignKey('service_accounts.id', ondelete='CASCADE'), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True, index=True)
    key_prefix = Column(String(20), nullable=False, index=True)
    key_name = Column(String(255), nullable=True)
    permissions = Column(JSONB, nullable=True)
    rate_limit = Column(JSONB, default={'requests_per_second': 100, 'burst': 200})
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    last_used_ip = Column(INET, nullable=True)
    revoked = Column(Boolean, default=False, nullable=False, index=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    revoked_by = Column(String(255), nullable=True)
    revoked_reason = Column(Text, nullable=True)
    metadata = Column(JSONB, default={})
    
    # Relationships
    service_account = relationship("ServiceAccount", back_populates="api_keys")
    audit_logs = relationship("SecretAuditLog", back_populates="api_key")
    
    # Indexes
    __table_args__ = (
        Index('idx_api_keys_service_account', 'service_account_id'),
        Index('idx_api_keys_key_hash', 'key_hash'),
        Index('idx_api_keys_key_prefix', 'key_prefix'),
        Index('idx_api_keys_expires_at', 'expires_at'),
        Index('idx_api_keys_revoked', 'revoked'),
    )
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, prefix={self.key_prefix}, revoked={self.revoked})>"


# ============================================================================
# SECRETS METADATA
# ============================================================================

class SecretMetadata(Base):
    """Secret metadata model"""
    
    __tablename__ = "secrets_metadata"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    path = Column(String(500), nullable=False, unique=True, index=True)
    cipher_id = Column(UUID(as_uuid=True), nullable=True)
    description = Column(Text, nullable=True)
    secret_type = Column(String(50), default='generic')
    rotation_enabled = Column(Boolean, default=False, index=True)
    rotation_policy_id = Column(UUID(as_uuid=True), ForeignKey('rotation_policies.id'), nullable=True)
    current_version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(255), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)
    tags = Column(ARRAY(Text), default=[])
    metadata = Column(JSONB, default={})
    active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    versions = relationship("SecretVersion", back_populates="secret", cascade="all, delete-orphan")
    rotation_policy = relationship("RotationPolicy", back_populates="secrets")
    audit_logs = relationship("SecretAuditLog", back_populates="secret")
    
    # Indexes
    __table_args__ = (
        Index('idx_secrets_metadata_path', 'path'),
        Index('idx_secrets_metadata_path_prefix', 'path', postgresql_ops={'path': 'text_pattern_ops'}),
        Index('idx_secrets_metadata_cipher_id', 'cipher_id'),
        Index('idx_secrets_metadata_rotation_enabled', 'rotation_enabled'),
        Index('idx_secrets_metadata_expires_at', 'expires_at'),
        Index('idx_secrets_metadata_tags', 'tags', postgresql_using='gin'),
        Index('idx_secrets_metadata_metadata', 'metadata', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<SecretMetadata(id={self.id}, path={self.path}, version={self.current_version})>"


# ============================================================================
# SECRET VERSIONS
# ============================================================================

class SecretVersion(Base):
    """Secret version model"""
    
    __tablename__ = "secret_versions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    secret_id = Column(UUID(as_uuid=True), ForeignKey('secrets_metadata.id', ondelete='CASCADE'), nullable=False)
    version = Column(Integer, nullable=False)
    cipher_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(255), nullable=True)
    creation_method = Column(String(50), default='manual')
    active = Column(Boolean, default=False, nullable=False)
    metadata = Column(JSONB, default={})
    
    # Relationships
    secret = relationship("SecretMetadata", back_populates="versions")
    
    # Indexes
    __table_args__ = (
        Index('idx_secret_versions_secret_id', 'secret_id'),
        Index('idx_secret_versions_version', 'secret_id', 'version', unique=True),
        Index('idx_secret_versions_active', 'secret_id', 'active'),
        Index('idx_secret_versions_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<SecretVersion(id={self.id}, secret_id={self.secret_id}, version={self.version}, active={self.active})>"


# ============================================================================
# ROTATION POLICIES
# ============================================================================

class RotationPolicy(Base):
    """Rotation policy model"""
    
    __tablename__ = "rotation_policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    secret_path = Column(String(500), nullable=False, index=True)
    rotation_interval_days = Column(Integer, nullable=False)
    rotation_window = Column(String(50), default='02:00-04:00')
    target_system = Column(JSONB, nullable=False)
    health_check = Column(JSONB, nullable=True)
    notification = Column(JSONB, default={})
    rollback_on_failure = Column(Boolean, default=True)
    last_rotation = Column(DateTime(timezone=True), nullable=True)
    next_rotation = Column(DateTime(timezone=True), nullable=True, index=True)
    rotation_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    metadata = Column(JSONB, default={})
    
    # Relationships
    secrets = relationship("SecretMetadata", back_populates="rotation_policy")
    rotation_history = relationship("RotationHistory", back_populates="rotation_policy", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_rotation_policies_secret_path', 'secret_path'),
        Index('idx_rotation_policies_next_rotation', 'next_rotation'),
        Index('idx_rotation_policies_active', 'active'),
    )
    
    def __repr__(self):
        return f"<RotationPolicy(id={self.id}, name={self.name}, active={self.active})>"


# ============================================================================
# ROTATION HISTORY
# ============================================================================

class RotationHistory(Base):
    """Rotation history model"""
    
    __tablename__ = "rotation_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    rotation_policy_id = Column(UUID(as_uuid=True), ForeignKey('rotation_policies.id', ondelete='CASCADE'), nullable=False)
    secret_id = Column(UUID(as_uuid=True), ForeignKey('secrets_metadata.id', ondelete='CASCADE'), nullable=False)
    old_version = Column(Integer, nullable=True)
    new_version = Column(Integer, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    health_check_result = Column(JSONB, nullable=True)
    rollback_reason = Column(Text, nullable=True)
    triggered_by = Column(String(255), nullable=True)
    metadata = Column(JSONB, default={})
    
    # Relationships
    rotation_policy = relationship("RotationPolicy", back_populates="rotation_history")
    
    # Indexes
    __table_args__ = (
        Index('idx_rotation_history_policy', 'rotation_policy_id'),
        Index('idx_rotation_history_secret', 'secret_id'),
        Index('idx_rotation_history_started_at', 'started_at'),
        Index('idx_rotation_history_status', 'status'),
    )
    
    def __repr__(self):
        return f"<RotationHistory(id={self.id}, status={self.status}, started_at={self.started_at})>"


# ============================================================================
# SECRET AUDIT LOG
# ============================================================================

class SecretAuditLog(Base):
    """Secret audit log model"""
    
    __tablename__ = "secret_audit_log"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    secret_path = Column(String(500), nullable=False, index=True)
    secret_id = Column(UUID(as_uuid=True), ForeignKey('secrets_metadata.id', ondelete='SET NULL'), nullable=True)
    action = Column(String(50), nullable=False, index=True)
    actor = Column(String(255), nullable=False, index=True)
    actor_type = Column(String(50), nullable=False)
    api_key_id = Column(UUID(as_uuid=True), ForeignKey('api_keys.id', ondelete='SET NULL'), nullable=True)
    service_account_id = Column(UUID(as_uuid=True), ForeignKey('service_accounts.id', ondelete='SET NULL'), nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    success = Column(Boolean, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    version_accessed = Column(Integer, nullable=True)
    request_id = Column(String(100), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    metadata = Column(JSONB, default={})
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    secret = relationship("SecretMetadata", back_populates="audit_logs")
    api_key = relationship("APIKey", back_populates="audit_logs")
    service_account = relationship("ServiceAccount", back_populates="audit_logs")
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_secret_path', 'secret_path'),
        Index('idx_audit_secret_id', 'secret_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_actor', 'actor'),
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_success', 'success'),
        Index('idx_audit_service_account', 'service_account_id'),
    )
    
    def __repr__(self):
        return f"<SecretAuditLog(id={self.id}, action={self.action}, actor={self.actor}, timestamp={self.timestamp})>"

