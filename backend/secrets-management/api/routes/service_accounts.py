"""
Service Accounts API Routes

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

FastAPI routes for service account management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from uuid import UUID

from api.schemas.service_account import (
    ServiceAccountCreate,
    ServiceAccountUpdate,
    ServiceAccountResponse,
    ServiceAccountWithKey,
    ServiceAccountListResponse,
    APIKeyCreate,
    APIKeyResponse,
    APIKeyWithSecret,
    APIKeyListResponse,
    APIKeyRevoke,
    ServiceAccountStats
)
from services.service_account_manager import ServiceAccountManager
from config.database import get_db
from api.middleware.auth import get_current_user  # To be implemented

router = APIRouter()


# ============================================================================
# SERVICE ACCOUNT ENDPOINTS
# ============================================================================

@router.post(
    "/",
    response_model=ServiceAccountWithKey,
    status_code=status.HTTP_201_CREATED,
    summary="Create Service Account",
    description="Create a new service account with an initial API key"
)
async def create_service_account(
    account: ServiceAccountCreate,
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db)),
    # current_user: str = Depends(get_current_user)  # Uncomment when auth is ready
):
    """
    Create a new service account
    
    - **name**: Unique service account name (alphanumeric, hyphens, underscores)
    - **description**: Optional description
    - **permissions**: Access permissions (paths, actions, deny_paths)
    - **rate_limit**: Optional custom rate limit
    - **metadata**: Additional metadata (tags, team, environment, etc.)
    
    Returns the created service account with an API key (shown only once!)
    
    **Example:**
    ```json
    {
      "name": "api-server-production",
      "description": "Production API server",
      "permissions": {
        "paths": ["production/database/*", "production/api-keys/*"],
        "actions": ["read"]
      },
      "metadata": {
        "team": "backend",
        "environment": "production"
      }
    }
    ```
    """
    try:
        result = await db.create_service_account(
            account,
            created_by="system"  # Replace with current_user when auth is ready
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
            detail=f"Failed to create service account: {str(e)}"
        )


@router.get(
    "/",
    response_model=ServiceAccountListResponse,
    summary="List Service Accounts",
    description="Get a paginated list of service accounts"
)
async def list_service_accounts(
    active_only: bool = Query(True, description="Only active accounts"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(50, ge=1, le=100, description="Results per page"),
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    List all service accounts with pagination
    
    - **active_only**: Filter for active accounts only (default: true)
    - **page**: Page number starting from 1
    - **page_size**: Number of results per page (1-100)
    
    Returns paginated list of service accounts
    """
    try:
        accounts, total = await db.list_service_accounts(active_only, page, page_size)
        
        return ServiceAccountListResponse(
            items=accounts,
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list service accounts: {str(e)}"
        )


@router.get(
    "/{account_id}",
    response_model=ServiceAccountResponse,
    summary="Get Service Account",
    description="Get a single service account by ID"
)
async def get_service_account(
    account_id: UUID,
    include_stats: bool = Query(False, description="Include usage statistics"),
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    Get service account details by ID
    
    - **account_id**: Service account UUID
    - **include_stats**: Include usage statistics (total keys, API calls, etc.)
    
    Returns service account details
    """
    account = await db.get_service_account(account_id, include_stats)
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service account {account_id} not found"
        )
    
    return account


@router.put(
    "/{account_id}",
    response_model=ServiceAccountResponse,
    summary="Update Service Account",
    description="Update service account properties"
)
async def update_service_account(
    account_id: UUID,
    update_data: ServiceAccountUpdate,
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    Update service account
    
    - **account_id**: Service account UUID
    - **description**: New description (optional)
    - **permissions**: New permissions (optional)
    - **rate_limit**: New rate limit (optional)
    - **active**: Active status (optional)
    - **metadata**: New metadata (optional)
    
    Returns updated service account
    
    **Note:** Only provided fields are updated (partial update)
    """
    try:
        account = await db.update_service_account(account_id, update_data)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service account {account_id} not found"
            )
        
        return account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update service account: {str(e)}"
        )


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Service Account",
    description="Delete a service account (cascades to API keys)"
)
async def delete_service_account(
    account_id: UUID,
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    Delete service account
    
    - **account_id**: Service account UUID
    
    **Warning:** This will also delete all API keys for this service account
    """
    deleted = await db.delete_service_account(account_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service account {account_id} not found"
        )
    
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )


# ============================================================================
# API KEY ENDPOINTS
# ============================================================================

@router.post(
    "/{account_id}/keys",
    response_model=APIKeyWithSecret,
    status_code=status.HTTP_201_CREATED,
    summary="Generate API Key",
    description="Generate a new API key for service account"
)
async def generate_api_key(
    account_id: UUID,
    key_data: APIKeyCreate,
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    Generate a new API key for service account
    
    - **account_id**: Service account UUID
    - **name**: Friendly name for the key (optional)
    - **permissions**: Override service account permissions (optional)
    - **expires_at**: Expiration date (optional)
    - **rate_limit**: Custom rate limit (optional)
    - **metadata**: Additional metadata (optional)
    
    Returns the generated API key (shown only once!)
    
    **Example:**
    ```json
    {
      "name": "Production API Key #2",
      "expires_at": "2026-01-01T00:00:00Z",
      "metadata": {
        "purpose": "secondary-key",
        "created_for": "failover"
      }
    }
    ```
    """
    try:
        api_key = await db.generate_api_key(account_id, key_data)
        return api_key
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate API key: {str(e)}"
        )


@router.get(
    "/{account_id}/keys",
    response_model=APIKeyListResponse,
    summary="List API Keys",
    description="List all API keys for service account"
)
async def list_api_keys(
    account_id: UUID,
    active_only: bool = Query(True, description="Only non-revoked, non-expired keys"),
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    List API keys for service account
    
    - **account_id**: Service account UUID
    - **active_only**: Only active keys (not revoked, not expired)
    
    Returns list of API keys (without secrets)
    """
    try:
        keys = await db.list_api_keys(account_id, active_only)
        
        return APIKeyListResponse(
            items=keys,
            total=len(keys),
            page=1,
            page_size=len(keys),
            has_next=False
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list API keys: {str(e)}"
        )


@router.delete(
    "/{account_id}/keys/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke API Key",
    description="Revoke (deactivate) an API key"
)
async def revoke_api_key(
    account_id: UUID,
    key_id: UUID,
    revoke_data: Optional[APIKeyRevoke] = None,
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    Revoke an API key
    
    - **account_id**: Service account UUID
    - **key_id**: API key UUID
    - **reason**: Optional revocation reason
    
    **Note:** Revoked keys cannot be un-revoked. Generate a new key if needed.
    """
    reason = revoke_data.reason if revoke_data else None
    
    revoked = await db.revoke_api_key(
        key_id,
        reason=reason,
        revoked_by="system"  # Replace with current_user when auth is ready
    )
    
    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key {key_id} not found"
        )
    
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get(
    "/{account_id}/stats",
    response_model=ServiceAccountStats,
    summary="Get Statistics",
    description="Get usage statistics for service account"
)
async def get_service_account_stats(
    account_id: UUID,
    db: ServiceAccountManager = Depends(lambda db=Depends(get_db): ServiceAccountManager(db))
):
    """
    Get usage statistics for service account
    
    - **account_id**: Service account UUID
    
    Returns:
    - Total API keys (all time)
    - Active API keys (current)
    - Total API calls (all time)
    - API calls in last 24 hours
    - Failed API calls
    - Last activity timestamp
    """
    stats = await db.get_statistics(account_id)
    
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service account {account_id} not found"
        )
    
    return stats


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get(
    "/health/check",
    summary="Health Check",
    description="Check if service accounts API is healthy",
    tags=["Health"]
)
async def health_check():
    """Simple health check for service accounts API"""
    return {
        "status": "healthy",
        "service": "service-accounts-api",
        "version": "1.0.0"
    }

