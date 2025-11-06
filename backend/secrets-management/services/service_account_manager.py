"""
Service Account Manager

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

Business logic for service account and API key management
"""

import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, func
from sqlalchemy.orm import selectinload

from database.models import ServiceAccount, APIKey
from api.schemas.service_account import (
    ServiceAccountCreate,
    ServiceAccountUpdate,
    ServiceAccountResponse,
    ServiceAccountWithKey,
    APIKeyCreate,
    APIKeyResponse,
    APIKeyWithSecret,
    ServiceAccountStats
)
from config.settings import get_settings

settings = get_settings()


class ServiceAccountManager:
    """Manager for service account operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ========================================================================
    # SERVICE ACCOUNT OPERATIONS
    # ========================================================================
    
    async def create_service_account(
        self,
        data: ServiceAccountCreate,
        created_by: Optional[str] = None
    ) -> ServiceAccountWithKey:
        """
        Create a new service account with initial API key
        
        Args:
            data: Service account creation data
            created_by: User or system creating the account
            
        Returns:
            ServiceAccountWithKey: Created account with API key
            
        Raises:
            ValueError: If service account name already exists
        """
        # Check if name already exists
        existing = await self.get_by_name(data.name)
        if existing:
            raise ValueError(f"Service account '{data.name}' already exists")
        
        # Create service account
        service_account = ServiceAccount(
            name=data.name,
            description=data.description,
            permissions=data.permissions.dict(),
            created_by=created_by,
            metadata=data.metadata,
            active=True
        )
        
        self.db.add(service_account)
        await self.db.flush()  # Get ID without committing
        
        # Generate initial API key
        api_key_data = APIKeyCreate(
            name=f"Initial key for {data.name}",
            permissions=None,  # Inherit from service account
            rate_limit=data.rate_limit
        )
        
        api_key, key_secret = await self._create_api_key(
            service_account.id,
            api_key_data
        )
        
        await self.db.commit()
        await self.db.refresh(service_account)
        
        # Return service account with API key
        return ServiceAccountWithKey(
            id=service_account.id,
            name=service_account.name,
            description=service_account.description,
            permissions=service_account.permissions,
            rate_limit=data.rate_limit.dict() if data.rate_limit else None,
            created_at=service_account.created_at,
            created_by=service_account.created_by,
            updated_at=service_account.updated_at,
            last_used_at=service_account.last_used_at,
            active=service_account.active,
            metadata=service_account.metadata,
            api_key=key_secret  # Only shown once!
        )
    
    async def get_service_account(
        self,
        account_id: UUID,
        include_stats: bool = False
    ) -> Optional[ServiceAccountResponse]:
        """
        Get service account by ID
        
        Args:
            account_id: Service account UUID
            include_stats: Include usage statistics
            
        Returns:
            ServiceAccountResponse or None if not found
        """
        query = select(ServiceAccount).where(ServiceAccount.id == account_id)
        result = await self.db.execute(query)
        account = result.scalar_one_or_none()
        
        if not account:
            return None
        
        response_data = {
            "id": account.id,
            "name": account.name,
            "description": account.description,
            "permissions": account.permissions,
            "created_at": account.created_at,
            "created_by": account.created_by,
            "updated_at": account.updated_at,
            "last_used_at": account.last_used_at,
            "active": account.active,
            "metadata": account.metadata,
        }
        
        if include_stats:
            stats = await self.get_statistics(account_id)
            if stats:
                response_data.update({
                    "total_keys": stats.total_keys,
                    "active_keys": stats.active_keys,
                    "total_api_calls": stats.total_api_calls,
                })
        
        return ServiceAccountResponse(**response_data)
    
    async def get_by_name(self, name: str) -> Optional[ServiceAccount]:
        """Get service account by name"""
        query = select(ServiceAccount).where(ServiceAccount.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def list_service_accounts(
        self,
        active_only: bool = True,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[ServiceAccountResponse], int]:
        """
        List service accounts with pagination
        
        Args:
            active_only: Filter for active accounts only
            page: Page number (1-indexed)
            page_size: Results per page
            
        Returns:
            Tuple of (accounts list, total count)
        """
        # Build query
        query = select(ServiceAccount)
        
        if active_only:
            query = query.where(ServiceAccount.active == True)
        
        # Get total count
        count_query = select(func.count()).select_from(ServiceAccount)
        if active_only:
            count_query = count_query.where(ServiceAccount.active == True)
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        query = query.offset((page - 1) * page_size).limit(page_size)
        query = query.order_by(ServiceAccount.created_at.desc())
        
        result = await self.db.execute(query)
        accounts = result.scalars().all()
        
        # Convert to response models
        response_list = [
            ServiceAccountResponse(
                id=account.id,
                name=account.name,
                description=account.description,
                permissions=account.permissions,
                created_at=account.created_at,
                created_by=account.created_by,
                updated_at=account.updated_at,
                last_used_at=account.last_used_at,
                active=account.active,
                metadata=account.metadata
            )
            for account in accounts
        ]
        
        return response_list, total
    
    async def update_service_account(
        self,
        account_id: UUID,
        data: ServiceAccountUpdate
    ) -> Optional[ServiceAccountResponse]:
        """
        Update service account
        
        Args:
            account_id: Service account UUID
            data: Update data
            
        Returns:
            Updated ServiceAccountResponse or None if not found
        """
        # Build update dict (only non-None values)
        update_data = {}
        if data.description is not None:
            update_data['description'] = data.description
        if data.permissions is not None:
            update_data['permissions'] = data.permissions.dict()
        if data.active is not None:
            update_data['active'] = data.active
        if data.metadata is not None:
            update_data['metadata'] = data.metadata
        
        if not update_data:
            # Nothing to update
            return await self.get_service_account(account_id)
        
        # Update in database
        stmt = (
            update(ServiceAccount)
            .where(ServiceAccount.id == account_id)
            .values(**update_data)
            .returning(ServiceAccount)
        )
        
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        account = result.scalar_one_or_none()
        if not account:
            return None
        
        return await self.get_service_account(account_id)
    
    async def delete_service_account(self, account_id: UUID) -> bool:
        """
        Delete service account (cascades to API keys)
        
        Args:
            account_id: Service account UUID
            
        Returns:
            True if deleted, False if not found
        """
        stmt = delete(ServiceAccount).where(ServiceAccount.id == account_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    # ========================================================================
    # API KEY OPERATIONS
    # ========================================================================
    
    async def _create_api_key(
        self,
        service_account_id: UUID,
        data: APIKeyCreate
    ) -> Tuple[APIKey, str]:
        """
        Internal method to create API key
        
        Args:
            service_account_id: Service account UUID
            data: API key creation data
            
        Returns:
            Tuple of (APIKey model, plaintext API key)
        """
        # Generate API key
        api_key_secret = self._generate_api_key()
        key_hash = self._hash_api_key(api_key_secret)
        key_prefix = api_key_secret[:20]  # First 20 chars for identification
        
        # Create API key record
        api_key = APIKey(
            service_account_id=service_account_id,
            key_hash=key_hash,
            key_prefix=key_prefix,
            key_name=data.name,
            permissions=data.permissions.dict() if data.permissions else None,
            rate_limit=data.rate_limit.dict() if data.rate_limit else None,
            expires_at=data.expires_at,
            metadata=data.metadata,
            revoked=False
        )
        
        self.db.add(api_key)
        await self.db.flush()
        
        return api_key, api_key_secret
    
    async def generate_api_key(
        self,
        service_account_id: UUID,
        data: APIKeyCreate
    ) -> APIKeyWithSecret:
        """
        Generate a new API key for service account
        
        Args:
            service_account_id: Service account UUID
            data: API key creation data
            
        Returns:
            APIKeyWithSecret: API key info with secret
            
        Raises:
            ValueError: If service account not found
        """
        # Verify service account exists
        account = await self.get_service_account(service_account_id)
        if not account:
            raise ValueError(f"Service account {service_account_id} not found")
        
        # Create API key
        api_key, key_secret = await self._create_api_key(service_account_id, data)
        
        await self.db.commit()
        await self.db.refresh(api_key)
        
        return APIKeyWithSecret(
            id=api_key.id,
            service_account_id=api_key.service_account_id,
            key_prefix=api_key.key_prefix,
            key_name=api_key.key_name,
            permissions=api_key.permissions,
            rate_limit=api_key.rate_limit,
            expires_at=api_key.expires_at,
            created_at=api_key.created_at,
            last_used_at=api_key.last_used_at,
            last_used_ip=str(api_key.last_used_ip) if api_key.last_used_ip else None,
            revoked=api_key.revoked,
            metadata=api_key.metadata,
            api_key=key_secret  # Only shown once!
        )
    
    async def list_api_keys(
        self,
        service_account_id: UUID,
        active_only: bool = True
    ) -> List[APIKeyResponse]:
        """
        List API keys for service account
        
        Args:
            service_account_id: Service account UUID
            active_only: Only non-revoked, non-expired keys
            
        Returns:
            List of APIKeyResponse
        """
        query = select(APIKey).where(APIKey.service_account_id == service_account_id)
        
        if active_only:
            now = datetime.utcnow()
            query = query.where(
                and_(
                    APIKey.revoked == False,
                    or_(
                        APIKey.expires_at.is_(None),
                        APIKey.expires_at > now
                    )
                )
            )
        
        query = query.order_by(APIKey.created_at.desc())
        
        result = await self.db.execute(query)
        keys = result.scalars().all()
        
        return [
            APIKeyResponse(
                id=key.id,
                service_account_id=key.service_account_id,
                key_prefix=key.key_prefix,
                key_name=key.key_name,
                permissions=key.permissions,
                rate_limit=key.rate_limit,
                expires_at=key.expires_at,
                created_at=key.created_at,
                last_used_at=key.last_used_at,
                last_used_ip=str(key.last_used_ip) if key.last_used_ip else None,
                revoked=key.revoked,
                metadata=key.metadata
            )
            for key in keys
        ]
    
    async def revoke_api_key(
        self,
        key_id: UUID,
        reason: Optional[str] = None,
        revoked_by: Optional[str] = None
    ) -> bool:
        """
        Revoke an API key
        
        Args:
            key_id: API key UUID
            reason: Revocation reason
            revoked_by: Who revoked it
            
        Returns:
            True if revoked, False if not found
        """
        stmt = (
            update(APIKey)
            .where(APIKey.id == key_id)
            .values(
                revoked=True,
                revoked_at=datetime.utcnow(),
                revoked_reason=reason,
                revoked_by=revoked_by
            )
        )
        
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    # ========================================================================
    # AUTHENTICATION & VALIDATION
    # ========================================================================
    
    async def validate_api_key(
        self,
        api_key: str,
        ip_address: Optional[str] = None
    ) -> Optional[Tuple[ServiceAccount, APIKey]]:
        """
        Validate API key and return service account
        
        Args:
            api_key: API key to validate
            ip_address: Request IP address
            
        Returns:
            Tuple of (ServiceAccount, APIKey) if valid, None otherwise
        """
        # Extract prefix for lookup (first 20 chars)
        key_prefix = api_key[:20]
        
        # Find API key by prefix
        query = select(APIKey).where(APIKey.key_prefix == key_prefix)
        query = query.options(selectinload(APIKey.service_account))
        
        result = await self.db.execute(query)
        db_key = result.scalar_one_or_none()
        
        if not db_key:
            return None
        
        # Check if revoked
        if db_key.revoked:
            return None
        
        # Check if expired
        if db_key.expires_at and db_key.expires_at <= datetime.utcnow():
            return None
        
        # Verify hash (constant-time comparison via bcrypt)
        if not self._verify_api_key(api_key, db_key.key_hash):
            return None
        
        # Check if service account is active
        if not db_key.service_account.active:
            return None
        
        # Update last used timestamp and IP
        await self._update_api_key_usage(db_key.id, ip_address)
        await self._update_service_account_usage(db_key.service_account_id)
        
        return db_key.service_account, db_key
    
    async def _update_api_key_usage(
        self,
        key_id: UUID,
        ip_address: Optional[str]
    ):
        """Update API key last used timestamp"""
        update_data = {"last_used_at": datetime.utcnow()}
        if ip_address:
            update_data["last_used_ip"] = ip_address
        
        stmt = update(APIKey).where(APIKey.id == key_id).values(**update_data)
        await self.db.execute(stmt)
        await self.db.commit()
    
    async def _update_service_account_usage(self, account_id: UUID):
        """Update service account last used timestamp"""
        stmt = (
            update(ServiceAccount)
            .where(ServiceAccount.id == account_id)
            .values(last_used_at=datetime.utcnow())
        )
        await self.db.execute(stmt)
        await self.db.commit()
    
    # ========================================================================
    # STATISTICS
    # ========================================================================
    
    async def get_statistics(
        self,
        service_account_id: UUID
    ) -> Optional[ServiceAccountStats]:
        """
        Get usage statistics for service account
        
        Args:
            service_account_id: Service account UUID
            
        Returns:
            ServiceAccountStats or None if not found
        """
        # This would query the service_account_stats view
        # For now, let's do a simple aggregation
        from database.models import SecretAuditLog
        
        account = await self.get_service_account(service_account_id)
        if not account:
            return None
        
        # Count API keys
        total_keys_query = select(func.count()).select_from(APIKey).where(
            APIKey.service_account_id == service_account_id
        )
        total_keys = (await self.db.execute(total_keys_query)).scalar()
        
        active_keys_query = select(func.count()).select_from(APIKey).where(
            and_(
                APIKey.service_account_id == service_account_id,
                APIKey.revoked == False
            )
        )
        active_keys = (await self.db.execute(active_keys_query)).scalar()
        
        # Count API calls from audit log
        total_calls_query = select(func.count()).select_from(SecretAuditLog).where(
            SecretAuditLog.service_account_id == service_account_id
        )
        total_calls = (await self.db.execute(total_calls_query)).scalar()
        
        # Calls in last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_calls_query = select(func.count()).select_from(SecretAuditLog).where(
            and_(
                SecretAuditLog.service_account_id == service_account_id,
                SecretAuditLog.timestamp >= yesterday
            )
        )
        recent_calls = (await self.db.execute(recent_calls_query)).scalar()
        
        # Failed calls
        failed_calls_query = select(func.count()).select_from(SecretAuditLog).where(
            and_(
                SecretAuditLog.service_account_id == service_account_id,
                SecretAuditLog.success == False
            )
        )
        failed_calls = (await self.db.execute(failed_calls_query)).scalar()
        
        return ServiceAccountStats(
            service_account_id=service_account_id,
            service_account_name=account.name,
            total_keys=total_keys or 0,
            active_keys=active_keys or 0,
            total_api_calls=total_calls or 0,
            calls_last_24h=recent_calls or 0,
            failed_calls=failed_calls or 0,
            last_used_at=account.last_used_at
        )
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _generate_api_key(self) -> str:
        """
        Generate a secure API key
        
        Returns:
            API key string with prefix
        """
        # Generate 32 bytes of random data
        random_bytes = secrets.token_urlsafe(32)
        
        # Add prefix for identification
        return f"{settings.API_KEY_PREFIX}{random_bytes}"
    
    def _hash_api_key(self, api_key: str) -> str:
        """
        Hash API key with bcrypt
        
        Args:
            api_key: Plaintext API key
            
        Returns:
            Bcrypt hash
        """
        return bcrypt.hashpw(
            api_key.encode('utf-8'),
            bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
        ).decode('utf-8')
    
    def _verify_api_key(self, api_key: str, key_hash: str) -> bool:
        """
        Verify API key against hash (constant-time)
        
        Args:
            api_key: Plaintext API key
            key_hash: Stored bcrypt hash
            
        Returns:
            True if valid, False otherwise
        """
        try:
            return bcrypt.checkpw(
                api_key.encode('utf-8'),
                key_hash.encode('utf-8')
            )
        except Exception:
            return False

