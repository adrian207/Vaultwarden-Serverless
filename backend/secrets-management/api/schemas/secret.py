"""
Secret Pydantic Schemas

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

Data validation and serialization for secrets
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID


# ============================================================================
# SECRET SCHEMAS
# ============================================================================

class SecretCreate(BaseModel):
    """Schema for creating a secret"""
    
    value: str = Field(
        ...,
        min_length=1,
        description="Secret value (will be encrypted)",
        example="my-secret-password-123"
    )
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Secret description",
        example="Production database password"
    )
    
    secret_type: str = Field(
        default="generic",
        description="Secret type",
        example="database"
    )
    
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for organization",
        example=["production", "database", "critical"]
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
        example={
            "environment": "production",
            "owner": "backend-team",
            "service": "api-server"
        }
    )
    
    expires_at: Optional[datetime] = Field(
        None,
        description="Expiration date (optional)",
        example="2026-01-01T00:00:00Z"
    )
    
    @validator("secret_type")
    def validate_secret_type(cls, v):
        """Validate secret type"""
        valid_types = {
            "generic", "password", "api_key", "database", 
            "ssh_key", "certificate", "token", "connection_string"
        }
        if v not in valid_types:
            raise ValueError(
                f"Invalid secret type '{v}'. Must be one of: {valid_types}"
            )
        return v
    
    @validator("expires_at")
    def validate_expires_at(cls, v):
        """Validate that expiration is in the future"""
        if v and v <= datetime.utcnow():
            raise ValueError("Expiration date must be in the future")
        return v
    
    @validator("tags")
    def validate_tags(cls, v):
        """Validate tags"""
        if len(v) > 20:
            raise ValueError("Maximum 20 tags allowed")
        for tag in v:
            if len(tag) > 50:
                raise ValueError("Tag length must be <= 50 characters")
        return v


class SecretUpdate(BaseModel):
    """Schema for updating a secret"""
    
    value: Optional[str] = Field(
        None,
        min_length=1,
        description="New secret value (creates new version)"
    )
    
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Secret description"
    )
    
    tags: Optional[List[str]] = Field(
        None,
        description="Tags"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata"
    )
    
    expires_at: Optional[datetime] = Field(
        None,
        description="Expiration date"
    )
    
    active: Optional[bool] = Field(
        None,
        description="Active status"
    )


class SecretResponse(BaseModel):
    """Schema for secret response (with value)"""
    
    id: UUID = Field(..., description="Secret ID")
    path: str = Field(..., description="Secret path")
    value: str = Field(..., description="Secret value (decrypted)")
    description: Optional[str] = Field(None, description="Description")
    secret_type: str = Field(..., description="Secret type")
    version: int = Field(..., description="Current version")
    tags: List[str] = Field(default_factory=list, description="Tags")
    metadata: Dict = Field(default_factory=dict, description="Metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    created_by: Optional[str] = Field(None, description="Creator")
    updated_at: datetime = Field(..., description="Last update timestamp")
    updated_by: Optional[str] = Field(None, description="Last updater")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    rotation_enabled: bool = Field(..., description="Rotation enabled")
    
    class Config:
        from_attributes = True


class SecretMetadataResponse(BaseModel):
    """Schema for secret response (without value)"""
    
    id: UUID = Field(..., description="Secret ID")
    path: str = Field(..., description="Secret path")
    description: Optional[str] = Field(None, description="Description")
    secret_type: str = Field(..., description="Secret type")
    version: int = Field(..., description="Current version")
    tags: List[str] = Field(default_factory=list, description="Tags")
    metadata: Dict = Field(default_factory=dict, description="Metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    created_by: Optional[str] = Field(None, description="Creator")
    updated_at: datetime = Field(..., description="Last update timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    rotation_enabled: bool = Field(..., description="Rotation enabled")
    
    class Config:
        from_attributes = True


# ============================================================================
# SECRET VERSION SCHEMAS
# ============================================================================

class SecretVersionResponse(BaseModel):
    """Schema for secret version response"""
    
    id: UUID = Field(..., description="Version ID")
    secret_id: UUID = Field(..., description="Secret ID")
    version: int = Field(..., description="Version number")
    created_at: datetime = Field(..., description="Creation timestamp")
    created_by: Optional[str] = Field(None, description="Creator")
    creation_method: str = Field(..., description="Creation method")
    active: bool = Field(..., description="Active version")
    metadata: Dict = Field(default_factory=dict, description="Version metadata")
    
    class Config:
        from_attributes = True


class SecretVersionWithValue(SecretVersionResponse):
    """Schema for secret version with value"""
    
    value: str = Field(..., description="Secret value (decrypted)")


class SecretVersionListResponse(BaseModel):
    """Schema for version history"""
    
    secret_id: UUID = Field(..., description="Secret ID")
    secret_path: str = Field(..., description="Secret path")
    current_version: int = Field(..., description="Current active version")
    versions: List[SecretVersionResponse] = Field(..., description="All versions")
    total_versions: int = Field(..., description="Total version count")


# ============================================================================
# SECRET LIST SCHEMAS
# ============================================================================

class SecretListItem(BaseModel):
    """Schema for secret list item (metadata only)"""
    
    path: str = Field(..., description="Secret path")
    description: Optional[str] = Field(None, description="Description")
    secret_type: str = Field(..., description="Secret type")
    version: int = Field(..., description="Current version")
    tags: List[str] = Field(default_factory=list, description="Tags")
    updated_at: datetime = Field(..., description="Last update")
    expires_at: Optional[datetime] = Field(None, description="Expiration")


class SecretListResponse(BaseModel):
    """Schema for paginated secret list"""
    
    items: List[SecretListItem] = Field(..., description="Secrets")
    total: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Has next page")
    prefix: Optional[str] = Field(None, description="Filter prefix")


# ============================================================================
# SECRET ROLLBACK SCHEMA
# ============================================================================

class SecretRollback(BaseModel):
    """Schema for rolling back to a previous version"""
    
    target_version: int = Field(
        ...,
        ge=1,
        description="Version number to rollback to",
        example=3
    )
    
    reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Reason for rollback",
        example="Previous version was incorrect"
    )


# ============================================================================
# BATCH OPERATIONS SCHEMAS
# ============================================================================

class SecretBatchGet(BaseModel):
    """Schema for batch get secrets"""
    
    paths: List[str] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="List of secret paths to retrieve",
        example=["production/db/password", "production/api/key"]
    )
    
    @validator("paths")
    def validate_paths(cls, v):
        """Validate paths"""
        for path in v:
            if not path or path.startswith("/"):
                raise ValueError("Invalid path format")
        return v


class SecretBatchGetResponse(BaseModel):
    """Schema for batch get response"""
    
    secrets: Dict[str, SecretResponse] = Field(
        ...,
        description="Map of path to secret"
    )
    
    errors: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of path to error message (for failed retrievals)"
    )


# ============================================================================
# SEARCH SCHEMAS
# ============================================================================

class SecretSearchQuery(BaseModel):
    """Schema for secret search"""
    
    prefix: Optional[str] = Field(
        None,
        description="Path prefix filter",
        example="production/"
    )
    
    tags: Optional[List[str]] = Field(
        None,
        description="Filter by tags (OR logic)",
        example=["production", "database"]
    )
    
    secret_type: Optional[str] = Field(
        None,
        description="Filter by secret type",
        example="database"
    )
    
    expires_before: Optional[datetime] = Field(
        None,
        description="Filter secrets expiring before this date"
    )
    
    created_after: Optional[datetime] = Field(
        None,
        description="Filter secrets created after this date"
    )
    
    page: int = Field(
        default=1,
        ge=1,
        description="Page number"
    )
    
    page_size: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Results per page"
    )


# ============================================================================
# STATISTICS SCHEMAS
# ============================================================================

class SecretStatistics(BaseModel):
    """Schema for secret statistics"""
    
    total_secrets: int = Field(..., description="Total secrets")
    active_secrets: int = Field(..., description="Active secrets")
    expired_secrets: int = Field(..., description="Expired secrets")
    secrets_with_rotation: int = Field(..., description="Secrets with rotation enabled")
    secrets_by_type: Dict[str, int] = Field(..., description="Count by type")
    total_versions: int = Field(..., description="Total versions across all secrets")
    average_versions_per_secret: float = Field(..., description="Average versions")
    recent_updates_24h: int = Field(..., description="Updates in last 24 hours")


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

def validate_secret_path(path: str) -> str:
    """
    Validate secret path format
    
    Rules:
    - No leading/trailing slashes
    - No double slashes
    - Only alphanumeric, hyphens, underscores, slashes
    - Max 500 characters
    
    Args:
        path: Secret path
        
    Returns:
        Validated path
        
    Raises:
        ValueError: If invalid
    """
    if not path:
        raise ValueError("Path cannot be empty")
    
    if path.startswith("/") or path.endswith("/"):
        raise ValueError("Path cannot start or end with '/'")
    
    if "//" in path:
        raise ValueError("Path cannot contain consecutive slashes")
    
    if len(path) > 500:
        raise ValueError("Path too long (max 500 characters)")
    
    import re
    if not re.match(r'^[a-zA-Z0-9/_-]+$', path):
        raise ValueError(
            "Path must contain only alphanumeric characters, "
            "hyphens, underscores, and slashes"
        )
    
    return path

