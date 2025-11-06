"""
Authentication Middleware

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05
Status: Stub - To be fully implemented in Sprint 1

API key authentication and authorization middleware
"""

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Tuple
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

from database.models import ServiceAccount, APIKey
from services.service_account_manager import ServiceAccountManager
from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger()

# HTTP Bearer token scheme
security = HTTPBearer(auto_error=False)


# ============================================================================
# AUTHENTICATION MIDDLEWARE (Class-based)
# ============================================================================

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to authenticate API requests using API keys
    
    **Status:** Stub implementation
    **TODO:** Implement full authentication logic in Sprint 1
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process each request for authentication
        
        Args:
            request: Incoming request
            call_next: Next middleware in chain
            
        Returns:
            Response from next middleware or error
        """
        # Skip authentication for certain paths
        skip_auth_paths = [
            "/health",
            "/ready",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/metrics"
        ]
        
        if any(request.url.path.startswith(path) for path in skip_auth_paths):
            return await call_next(request)
        
        # TODO: Implement API key extraction and validation
        # For now, allow all requests
        
        response = await call_next(request)
        return response


# ============================================================================
# DEPENDENCY FOR PROTECTED ROUTES
# ============================================================================

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> str:
    """
    Extract and validate current user from API key
    
    **Status:** Stub implementation
    **TODO:** Implement full authentication in Sprint 1
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        User/service account identifier
        
    Raises:
        HTTPException: If authentication fails
    """
    # TODO: Implement API key validation
    # For now, return a placeholder
    return "system"


async def get_current_service_account(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Tuple[ServiceAccount, APIKey]:
    """
    Extract and validate service account from API key
    
    **Status:** Stub implementation
    **TODO:** Implement full authentication in Sprint 1
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        Tuple of (ServiceAccount, APIKey)
        
    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract API key from Bearer token
    api_key = credentials.credentials
    
    # Get client IP
    client_ip = None
    if hasattr(db, "request"):
        client_ip = db.request.client.host
    
    # Validate API key
    manager = ServiceAccountManager(db)
    result = await manager.validate_api_key(api_key, client_ip)
    
    if not result:
        logger.warning(
            "authentication_failed",
            reason="invalid_api_key",
            key_prefix=api_key[:20] if len(api_key) >= 20 else api_key
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    service_account, api_key_record = result
    
    logger.info(
        "authentication_success",
        service_account=service_account.name,
        service_account_id=str(service_account.id)
    )
    
    return service_account, api_key_record


# ============================================================================
# PERMISSION CHECKING
# ============================================================================

def check_permission(
    service_account: ServiceAccount,
    api_key: APIKey,
    path: str,
    action: str
) -> bool:
    """
    Check if service account has permission for action on path
    
    **Status:** Stub implementation
    **TODO:** Implement full permission checking in Sprint 1
    
    Args:
        service_account: ServiceAccount instance
        api_key: APIKey instance
        path: Secret path
        action: Action (read, write, delete, rotate)
        
    Returns:
        True if allowed, False otherwise
    """
    # Get effective permissions (API key can override service account)
    permissions = api_key.permissions if api_key.permissions else service_account.permissions
    
    if not permissions:
        return False
    
    # Check if action is allowed
    allowed_actions = permissions.get("actions", [])
    if action not in allowed_actions:
        return False
    
    # Check if path is allowed
    allowed_paths = permissions.get("paths", [])
    denied_paths = permissions.get("deny_paths", [])
    
    # First check deny list (takes precedence)
    for deny_pattern in denied_paths:
        if _path_matches(path, deny_pattern):
            return False
    
    # Then check allow list
    for allow_pattern in allowed_paths:
        if _path_matches(path, allow_pattern):
            return True
    
    # Default deny
    return False


def _path_matches(path: str, pattern: str) -> bool:
    """
    Check if path matches pattern (with wildcard support)
    
    Args:
        path: Secret path (e.g., "production/database/password")
        pattern: Pattern (e.g., "production/*", "*/database/*")
        
    Returns:
        True if matches, False otherwise
    """
    import fnmatch
    return fnmatch.fnmatch(path, pattern)


# ============================================================================
# RATE LIMITING CHECK
# ============================================================================

async def check_rate_limit(
    service_account: ServiceAccount,
    api_key: APIKey
) -> bool:
    """
    Check if request is within rate limit
    
    **Status:** Stub implementation
    **TODO:** Implement rate limiting in Sprint 2
    
    Args:
        service_account: ServiceAccount instance
        api_key: APIKey instance
        
    Returns:
        True if within limits, False otherwise
    """
    # TODO: Implement actual rate limiting with Redis or in-memory store
    # For now, always allow
    return True


# ============================================================================
# AUTHORIZATION DEPENDENCY
# ============================================================================

class RequirePermission:
    """
    Dependency to require specific permission for an endpoint
    
    Usage:
        @app.get("/secrets/{path}")
        async def get_secret(
            path: str,
            auth: Tuple[ServiceAccount, APIKey] = Depends(RequirePermission("read"))
        ):
            # Only called if user has "read" permission
            pass
    """
    
    def __init__(self, action: str):
        self.action = action
    
    async def __call__(
        self,
        auth: Tuple[ServiceAccount, APIKey] = Depends(get_current_service_account)
    ) -> Tuple[ServiceAccount, APIKey]:
        """
        Check if authenticated user has required permission
        
        Args:
            auth: Authenticated service account and API key
            
        Returns:
            Tuple of (ServiceAccount, APIKey) if authorized
            
        Raises:
            HTTPException: If not authorized
        """
        service_account, api_key = auth
        
        # For now, just return the auth tuple
        # TODO: Implement actual permission checking in Sprint 1
        
        return service_account, api_key


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_api_key_from_request(request: Request) -> Optional[str]:
    """
    Extract API key from request headers
    
    Supports:
    - Authorization: Bearer <api-key>
    - X-API-Key: <api-key>
    
    Args:
        request: FastAPI request
        
    Returns:
        API key if found, None otherwise
    """
    # Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    # Check X-API-Key header
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header:
        return api_key_header
    
    return None


def extract_client_ip(request: Request) -> str:
    """
    Extract client IP from request
    
    Checks X-Forwarded-For header first (for proxies)
    
    Args:
        request: FastAPI request
        
    Returns:
        Client IP address
    """
    # Check X-Forwarded-For header (for proxies/load balancers)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take first IP in list
        return forwarded_for.split(",")[0].strip()
    
    # Fall back to direct client IP
    if request.client:
        return request.client.host
    
    return "unknown"


# ============================================================================
# NOTES FOR SPRINT 1 IMPLEMENTATION
# ============================================================================

"""
TODO for Sprint 1:

1. Implement full AuthMiddleware.dispatch():
   - Extract API key from headers
   - Validate against database
   - Add service account to request.state
   - Log authentication attempts

2. Implement check_permission():
   - Parse permission patterns
   - Support wildcards (*, **)
   - Handle deny list properly
   - Add permission caching

3. Implement rate limiting:
   - Use Redis for distributed limiting
   - Or in-memory for single instance
   - Track requests per API key
   - Return 429 Too Many Requests when exceeded

4. Add comprehensive logging:
   - Log all authentication attempts
   - Log permission checks
   - Log rate limit violations

5. Write unit tests:
   - Test API key validation
   - Test permission checking
   - Test rate limiting
   - Test edge cases
"""

