"""
Secrets API Routes

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

FastAPI routes for secret management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
from uuid import UUID

from api.schemas.secret import (
    SecretCreate,
    SecretUpdate,
    SecretResponse,
    SecretMetadataResponse,
    SecretListResponse,
    SecretListItem,
    SecretVersionResponse,
    SecretVersionListResponse,
    SecretRollback,
    SecretBatchGet,
    SecretBatchGetResponse,
    SecretSearchQuery,
    SecretStatistics,
    validate_secret_path
)
from services.secret_manager import SecretManager
from config.database import get_db
from api.middleware.auth import get_current_user, RequirePermission

router = APIRouter()


# ============================================================================
# SECRET CRUD ENDPOINTS
# ============================================================================

@router.post(
    "/{path:path}",
    response_model=SecretResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Secret",
    description="Create a new secret at the specified path"
)
async def create_secret(
    path: str = Path(..., description="Secret path (e.g., production/database/password)"),
    secret: SecretCreate = ...,
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)  # Uncomment when auth ready
):
    """
    Create a new secret
    
    - **path**: Hierarchical path (e.g., `production/database/password`)
    - **value**: Secret value (will be encrypted)
    - **description**: Optional description
    - **secret_type**: Type (generic, password, api_key, database, etc.)
    - **tags**: Tags for organization
    - **metadata**: Additional metadata
    - **expires_at**: Optional expiration date
    
    **Example:**
    ```json
    {
      "value": "my-secret-password-123",
      "description": "Production database password",
      "secret_type": "database",
      "tags": ["production", "critical"],
      "metadata": {
        "environment": "production",
        "owner": "backend-team"
      }
    }
    ```
    
    **Note:** Secret value is encrypted before storage
    """
    try:
        result = await db.create_secret(
            path,
            secret,
            created_by="system"  # Replace with current_user
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create secret: {str(e)}"
        )


@router.get(
    "/{path:path}",
    response_model=SecretResponse,
    summary="Get Secret",
    description="Retrieve a secret by path (returns decrypted value)"
)
async def get_secret(
    path: str = Path(..., description="Secret path"),
    version: Optional[int] = Query(None, description="Specific version (default: current)"),
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    Get a secret by path
    
    - **path**: Secret path
    - **version**: Optional specific version (default: current active version)
    
    Returns the decrypted secret value
    
    **Security:** Requires `read` permission on the secret path
    """
    try:
        secret = await db.get_secret(path, version)
        
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Secret '{path}' not found"
            )
        
        return secret
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve secret: {str(e)}"
        )


@router.put(
    "/{path:path}",
    response_model=SecretResponse,
    summary="Update Secret",
    description="Update a secret (creates new version if value changed)"
)
async def update_secret(
    path: str = Path(..., description="Secret path"),
    update_data: SecretUpdate = ...,
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    Update a secret
    
    - **path**: Secret path
    - **value**: New value (creates new version)
    - **description**: Update description
    - **tags**: Update tags
    - **metadata**: Update metadata
    - **expires_at**: Update expiration
    - **active**: Update active status
    
    **Note:** Updating the value creates a new version automatically
    
    **Security:** Requires `write` permission on the secret path
    """
    try:
        secret = await db.update_secret(
            path,
            update_data,
            updated_by="system"  # Replace with current_user
        )
        
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Secret '{path}' not found"
            )
        
        return secret
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update secret: {str(e)}"
        )


@router.delete(
    "/{path:path}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Secret",
    description="Delete a secret (soft delete by default)"
)
async def delete_secret(
    path: str = Path(..., description="Secret path"),
    hard_delete: bool = Query(False, description="Permanently delete (default: soft delete)"),
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    Delete a secret
    
    - **path**: Secret path
    - **hard_delete**: If true, permanently delete; else soft delete (mark as inactive)
    
    **Note:** Soft delete allows recovery; hard delete is permanent
    
    **Security:** Requires `delete` permission on the secret path
    """
    deleted = await db.delete_secret(path, hard_delete)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret '{path}' not found"
        )
    
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )


# ============================================================================
# SECRET LIST ENDPOINTS
# ============================================================================

@router.get(
    "/",
    response_model=SecretListResponse,
    summary="List Secrets",
    description="List secrets with filtering and pagination"
)
async def list_secrets(
    prefix: Optional[str] = Query(None, description="Path prefix filter (e.g., 'production/')"),
    tags: Optional[str] = Query(None, description="Comma-separated tags (OR logic)"),
    secret_type: Optional[str] = Query(None, description="Filter by secret type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Results per page"),
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    List secrets with filtering
    
    - **prefix**: Filter by path prefix (e.g., `production/`)
    - **tags**: Filter by tags (comma-separated, OR logic)
    - **secret_type**: Filter by type
    - **page**: Page number (1-indexed)
    - **page_size**: Results per page (1-100)
    
    Returns metadata only (no secret values for security)
    
    **Example:** List all production secrets:
    ```
    GET /api/v1/secrets?prefix=production/&page=1&page_size=50
    ```
    """
    try:
        # Parse tags
        tag_list = None
        if tags:
            tag_list = [t.strip() for t in tags.split(",")]
        
        items, total = await db.list_secrets(
            prefix=prefix,
            tags=tag_list,
            secret_type=secret_type,
            page=page,
            page_size=page_size
        )
        
        return SecretListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total,
            prefix=prefix
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list secrets: {str(e)}"
        )


# ============================================================================
# VERSION ENDPOINTS
# ============================================================================

@router.get(
    "/{path:path}/versions",
    response_model=SecretVersionListResponse,
    summary="Get Version History",
    description="Get all versions of a secret"
)
async def get_version_history(
    path: str = Path(..., description="Secret path"),
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    Get version history for a secret
    
    - **path**: Secret path
    
    Returns all versions (most recent first) without decrypted values
    
    **Security:** Requires `read` permission on the secret path
    """
    versions = await db.get_version_history(path)
    
    if versions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Secret '{path}' not found"
        )
    
    # Get secret metadata
    secret = await db.get_secret_by_path(path, include_value=False)
    
    return SecretVersionListResponse(
        secret_id=secret.id,
        secret_path=path,
        current_version=secret.version,
        versions=versions,
        total_versions=len(versions)
    )


@router.post(
    "/{path:path}/rollback",
    response_model=SecretResponse,
    summary="Rollback to Version",
    description="Rollback a secret to a previous version"
)
async def rollback_secret(
    path: str = Path(..., description="Secret path"),
    rollback_data: SecretRollback = ...,
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    Rollback secret to a previous version
    
    - **path**: Secret path
    - **target_version**: Version number to rollback to
    - **reason**: Optional reason for rollback
    
    Creates a new version that is a copy of the target version
    
    **Example:**
    ```json
    {
      "target_version": 3,
      "reason": "Previous version was incorrect"
    }
    ```
    
    **Security:** Requires `write` permission on the secret path
    """
    try:
        secret = await db.rollback_to_version(
            path,
            rollback_data.target_version,
            rolled_back_by="system"  # Replace with current_user
        )
        
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Secret '{path}' not found"
            )
        
        return secret
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rollback secret: {str(e)}"
        )


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

@router.post(
    "/batch/get",
    response_model=SecretBatchGetResponse,
    summary="Batch Get Secrets",
    description="Retrieve multiple secrets in a single request"
)
async def batch_get_secrets(
    request: SecretBatchGet = ...,
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    Get multiple secrets at once
    
    - **paths**: List of secret paths (max 100)
    
    Returns:
    - **secrets**: Map of path to SecretResponse (for successful retrievals)
    - **errors**: Map of path to error message (for failed retrievals)
    
    **Example:**
    ```json
    {
      "paths": [
        "production/database/password",
        "production/api/key",
        "production/stripe/secret"
      ]
    }
    ```
    
    **Security:** Checks `read` permission on each path individually
    """
    try:
        secrets, errors = await db.batch_get_secrets(request.paths)
        
        return SecretBatchGetResponse(
            secrets=secrets,
            errors=errors
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to batch get secrets: {str(e)}"
        )


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get(
    "/stats/overview",
    response_model=SecretStatistics,
    summary="Get Statistics",
    description="Get overall secret statistics"
)
async def get_statistics(
    db: SecretManager = Depends(lambda db=Depends(get_db): SecretManager(db)),
    # current_user: str = Depends(get_current_user)
):
    """
    Get overall secret statistics
    
    Returns:
    - Total secrets
    - Active (non-expired) secrets
    - Expired secrets
    - Secrets with rotation enabled
    - Secrets by type
    - Total versions
    - Average versions per secret
    - Recent updates (last 24 hours)
    
    **Security:** Requires admin permission
    """
    try:
        stats = await db.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get(
    "/health/check",
    summary="Health Check",
    description="Check if secrets API is healthy",
    tags=["Health"]
)
async def health_check():
    """Simple health check for secrets API"""
    return {
        "status": "healthy",
        "service": "secrets-api",
        "version": "1.0.0"
    }

