"""
Service Account Pydantic Schemas

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

Data validation and serialization for service accounts
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID


# ============================================================================
# PERMISSIONS SCHEMA
# ============================================================================

class Permissions(BaseModel):
    """Service account permissions model"""
    
    paths: List[str] = Field(
        default_factory=list,
        description="List of allowed paths (supports wildcards: production/*)",
        example=["production/database/*", "production/api-keys/*"]
    )
    
    deny_paths: List[str] = Field(
        default_factory=list,
        description="List of denied paths (takes precedence over paths)",
        example=["production/master-keys/*"]
    )
    
    actions: List[str] = Field(
        default=["read"],
        description="Allowed actions: read, write, delete, rotate",
        example=["read", "write"]
    )
    
    @validator("actions")
    def validate_actions(cls, v):
        """Validate that actions are valid"""
        valid_actions = {"read", "write", "delete", "rotate", "admin"}
        for action in v:
            if action not in valid_actions:
                raise ValueError(
                    f"Invalid action '{action}'. Must be one of: {valid_actions}"
                )
        return v
    
    @validator("paths", "deny_paths")
    def validate_paths(cls, v):
        """Validate path format"""
        for path in v:
            if not path:
                raise ValueError("Path cannot be empty")
            if path.startswith("/"):
                raise ValueError("Path should not start with '/'")
            # Check for invalid characters
            invalid_chars = [" ", "\t", "\n", "\r"]
            for char in invalid_chars:
                if char in path:
                    raise ValueError(f"Path contains invalid character: {repr(char)}")
        return v


# ============================================================================
# RATE LIMIT SCHEMA
# ============================================================================

class RateLimit(BaseModel):
    """Rate limit configuration"""
    
    requests_per_second: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Maximum requests per second",
        example=100
    )
    
    burst: int = Field(
        default=200,
        ge=1,
        le=20000,
        description="Maximum burst size",
        example=200
    )


# ============================================================================
# SERVICE ACCOUNT SCHEMAS
# ============================================================================

class ServiceAccountCreate(BaseModel):
    """Schema for creating a service account"""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Unique service account name",
        example="api-server-production"
    )
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Service account description",
        example="Production API server access"
    )
    
    permissions: Permissions = Field(
        default_factory=Permissions,
        description="Access permissions"
    )
    
    rate_limit: Optional[RateLimit] = Field(
        None,
        description="Custom rate limit (defaults to global settings)"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
        example={"team": "backend", "environment": "production"}
    )
    
    @validator("name")
    def validate_name(cls, v):
        """Validate service account name"""
        # Only alphanumeric, hyphens, underscores
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(
                "Name must contain only alphanumeric characters, hyphens, and underscores"
            )
        return v


class ServiceAccountUpdate(BaseModel):
    """Schema for updating a service account"""
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Service account description"
    )
    
    permissions: Optional[Permissions] = Field(
        None,
        description="Access permissions"
    )
    
    rate_limit: Optional[RateLimit] = Field(
        None,
        description="Custom rate limit"
    )
    
    active: Optional[bool] = Field(
        None,
        description="Active status"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata"
    )


class ServiceAccountResponse(BaseModel):
    """Schema for service account response"""
    
    id: UUID = Field(..., description="Service account ID")
    name: str = Field(..., description="Service account name")
    description: Optional[str] = Field(None, description="Description")
    permissions: Dict = Field(..., description="Permissions")
    rate_limit: Optional[Dict] = Field(None, description="Rate limit configuration")
    created_at: datetime = Field(..., description="Creation timestamp")
    created_by: Optional[str] = Field(None, description="Creator")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_used_at: Optional[datetime] = Field(None, description="Last use timestamp")
    active: bool = Field(..., description="Active status")
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")
    
    # Statistics (optional, populated from view)
    total_keys: Optional[int] = Field(None, description="Total API keys")
    active_keys: Optional[int] = Field(None, description="Active API keys")
    total_api_calls: Optional[int] = Field(None, description="Total API calls")
    
    class Config:
        from_attributes = True


class ServiceAccountWithKey(ServiceAccountResponse):
    """Schema for service account with API key (only on creation)"""
    
    api_key: str = Field(
        ...,
        description="API key (only shown once!)",
        example="vw_svc_abc123xyz..."
    )
    
    secret_key: Optional[str] = Field(
        None,
        description="Secret key for signing (optional, only shown once)"
    )


# ============================================================================
# API KEY SCHEMAS
# ============================================================================

class APIKeyCreate(BaseModel):
    """Schema for generating a new API key"""
    
    name: Optional[str] = Field(
        None,
        max_length=255,
        description="Friendly name for the API key",
        example="Production API Key #1"
    )
    
    permissions: Optional[Permissions] = Field(
        None,
        description="Override service account permissions (optional)"
    )
    
    expires_at: Optional[datetime] = Field(
        None,
        description="Expiration date (optional)",
        example="2026-01-01T00:00:00Z"
    )
    
    rate_limit: Optional[RateLimit] = Field(
        None,
        description="Custom rate limit for this key"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    
    @validator("expires_at")
    def validate_expires_at(cls, v):
        """Validate that expiration is in the future"""
        if v and v <= datetime.utcnow():
            raise ValueError("Expiration date must be in the future")
        return v


class APIKeyResponse(BaseModel):
    """Schema for API key response"""
    
    id: UUID = Field(..., description="API key ID")
    service_account_id: UUID = Field(..., description="Service account ID")
    key_prefix: str = Field(..., description="API key prefix (for identification)")
    key_name: Optional[str] = Field(None, description="Friendly name")
    permissions: Optional[Dict] = Field(None, description="Override permissions")
    rate_limit: Optional[Dict] = Field(None, description="Rate limit")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_used_at: Optional[datetime] = Field(None, description="Last use timestamp")
    last_used_ip: Optional[str] = Field(None, description="Last IP address")
    revoked: bool = Field(..., description="Revoked status")
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        from_attributes = True


class APIKeyWithSecret(APIKeyResponse):
    """Schema for API key with secret (only on creation)"""
    
    api_key: str = Field(
        ...,
        description="Full API key (only shown once!)",
        example="vw_svc_abc123xyz..."
    )


class APIKeyRevoke(BaseModel):
    """Schema for revoking an API key"""
    
    reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for revocation",
        example="Key compromised"
    )


# ============================================================================
# LIST SCHEMAS
# ============================================================================

class ServiceAccountListResponse(BaseModel):
    """Schema for paginated service account list"""
    
    items: List[ServiceAccountResponse] = Field(..., description="Service accounts")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Has next page")


class APIKeyListResponse(BaseModel):
    """Schema for paginated API key list"""
    
    items: List[APIKeyResponse] = Field(..., description="API keys")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Has next page")


# ============================================================================
# STATISTICS SCHEMAS
# ============================================================================

class ServiceAccountStats(BaseModel):
    """Service account usage statistics"""
    
    service_account_id: UUID
    service_account_name: str
    total_keys: int = Field(..., description="Total API keys")
    active_keys: int = Field(..., description="Active API keys")
    total_api_calls: int = Field(..., description="Total API calls")
    calls_last_24h: int = Field(..., description="API calls in last 24 hours")
    failed_calls: int = Field(..., description="Failed API calls")
    last_used_at: Optional[datetime] = Field(None, description="Last activity")
    
    class Config:
        from_attributes = True

