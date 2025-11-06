"""
Secret Manager

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

Business logic for secret management with encryption
"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, func
from sqlalchemy.orm import selectinload
import structlog

from database.models import SecretMetadata, SecretVersion
from api.schemas.secret import (
    SecretCreate,
    SecretUpdate,
    SecretResponse,
    SecretMetadataResponse,
    SecretVersionResponse,
    SecretListItem,
    SecretStatistics,
    validate_secret_path
)
from config.settings import get_settings

settings = get_settings()
logger = structlog.get_logger()


class SecretManager:
    """Manager for secret operations with encryption"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self._cipher = self._init_cipher()
    
    def _init_cipher(self) -> Fernet:
        """
        Initialize Fernet cipher for encryption/decryption
        
        Returns:
            Fernet cipher instance
        """
        # In production, get key from settings
        # For now, derive from ENCRYPTION_KEY setting
        key = settings.ENCRYPTION_KEY.encode()
        
        # If key is not proper length, derive it
        if len(key) != 32:
            # Derive a proper 32-byte key using PBKDF2
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'vaultwarden_secrets',  # In production, use unique salt
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(key))
        else:
            key = base64.urlsafe_b64encode(key)
        
        return Fernet(key)
    
    # ========================================================================
    # ENCRYPTION / DECRYPTION
    # ========================================================================
    
    def _encrypt(self, value: str) -> str:
        """
        Encrypt a secret value
        
        Args:
            value: Plaintext secret
            
        Returns:
            Base64-encoded encrypted value
        """
        encrypted = self._cipher.encrypt(value.encode('utf-8'))
        return base64.b64encode(encrypted).decode('utf-8')
    
    def _decrypt(self, encrypted_value: str) -> str:
        """
        Decrypt a secret value
        
        Args:
            encrypted_value: Base64-encoded encrypted value
            
        Returns:
            Plaintext secret
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_value)
            decrypted = self._cipher.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error("decryption_failed", error=str(e))
            raise ValueError("Failed to decrypt secret")
    
    # ========================================================================
    # SECRET OPERATIONS
    # ========================================================================
    
    async def create_secret(
        self,
        path: str,
        data: SecretCreate,
        created_by: Optional[str] = None
    ) -> SecretResponse:
        """
        Create a new secret
        
        Args:
            path: Secret path
            data: Secret data
            created_by: User creating the secret
            
        Returns:
            SecretResponse with encrypted value
            
        Raises:
            ValueError: If secret already exists or path invalid
        """
        # Validate path
        path = validate_secret_path(path)
        
        # Check if secret already exists
        existing = await self.get_secret_by_path(path, include_value=False)
        if existing:
            raise ValueError(f"Secret '{path}' already exists")
        
        # Encrypt the secret value
        encrypted_value = self._encrypt(data.value)
        
        # Create secret metadata
        secret = SecretMetadata(
            path=path,
            description=data.description,
            secret_type=data.secret_type,
            current_version=1,
            created_by=created_by,
            updated_by=created_by,
            expires_at=data.expires_at,
            tags=data.tags,
            metadata=data.metadata,
            rotation_enabled=False,
            active=True
        )
        
        self.db.add(secret)
        await self.db.flush()
        
        # Create first version
        version = SecretVersion(
            secret_id=secret.id,
            version=1,
            cipher_id=uuid4(),  # Placeholder - in real impl, store in Vaultwarden
            created_by=created_by,
            creation_method='manual',
            active=True,
            metadata={'encrypted_value': encrypted_value}  # Store encrypted value
        )
        
        self.db.add(version)
        await self.db.commit()
        await self.db.refresh(secret)
        
        logger.info(
            "secret_created",
            path=path,
            secret_id=str(secret.id),
            created_by=created_by
        )
        
        return SecretResponse(
            id=secret.id,
            path=secret.path,
            value=data.value,  # Return plaintext for convenience
            description=secret.description,
            secret_type=secret.secret_type,
            version=secret.current_version,
            tags=secret.tags,
            metadata=secret.metadata,
            created_at=secret.created_at,
            created_by=secret.created_by,
            updated_at=secret.updated_at,
            updated_by=secret.updated_by,
            expires_at=secret.expires_at,
            rotation_enabled=secret.rotation_enabled
        )
    
    async def get_secret(
        self,
        path: str,
        version: Optional[int] = None
    ) -> Optional[SecretResponse]:
        """
        Get a secret by path with decrypted value
        
        Args:
            path: Secret path
            version: Specific version (None = current)
            
        Returns:
            SecretResponse with decrypted value or None if not found
        """
        # Validate path
        path = validate_secret_path(path)
        
        # Get secret metadata
        query = select(SecretMetadata).where(
            and_(
                SecretMetadata.path == path,
                SecretMetadata.active == True
            )
        )
        result = await self.db.execute(query)
        secret = result.scalar_one_or_none()
        
        if not secret:
            return None
        
        # Check if expired
        if secret.expires_at and secret.expires_at <= datetime.utcnow():
            logger.warning("secret_expired", path=path)
            return None
        
        # Get version
        if version is None:
            version = secret.current_version
        
        version_query = select(SecretVersion).where(
            and_(
                SecretVersion.secret_id == secret.id,
                SecretVersion.version == version
            )
        )
        version_result = await self.db.execute(version_query)
        version_obj = version_result.scalar_one_or_none()
        
        if not version_obj:
            return None
        
        # Decrypt value
        encrypted_value = version_obj.metadata.get('encrypted_value', '')
        try:
            decrypted_value = self._decrypt(encrypted_value)
        except Exception as e:
            logger.error(
                "secret_decryption_failed",
                path=path,
                version=version,
                error=str(e)
            )
            raise
        
        return SecretResponse(
            id=secret.id,
            path=secret.path,
            value=decrypted_value,
            description=secret.description,
            secret_type=secret.secret_type,
            version=secret.current_version,
            tags=secret.tags,
            metadata=secret.metadata,
            created_at=secret.created_at,
            created_by=secret.created_by,
            updated_at=secret.updated_at,
            updated_by=secret.updated_by,
            expires_at=secret.expires_at,
            rotation_enabled=secret.rotation_enabled
        )
    
    async def get_secret_by_path(
        self,
        path: str,
        include_value: bool = True
    ) -> Optional[SecretMetadataResponse]:
        """
        Get secret metadata by path (without decryption)
        
        Args:
            path: Secret path
            include_value: Whether to decrypt and include value
            
        Returns:
            SecretMetadataResponse or None
        """
        query = select(SecretMetadata).where(
            and_(
                SecretMetadata.path == path,
                SecretMetadata.active == True
            )
        )
        result = await self.db.execute(query)
        secret = result.scalar_one_or_none()
        
        if not secret:
            return None
        
        return SecretMetadataResponse(
            id=secret.id,
            path=secret.path,
            description=secret.description,
            secret_type=secret.secret_type,
            version=secret.current_version,
            tags=secret.tags,
            metadata=secret.metadata,
            created_at=secret.created_at,
            created_by=secret.created_by,
            updated_at=secret.updated_at,
            expires_at=secret.expires_at,
            rotation_enabled=secret.rotation_enabled
        )
    
    async def update_secret(
        self,
        path: str,
        data: SecretUpdate,
        updated_by: Optional[str] = None
    ) -> Optional[SecretResponse]:
        """
        Update a secret (creates new version if value changed)
        
        Args:
            path: Secret path
            data: Update data
            updated_by: User updating the secret
            
        Returns:
            Updated SecretResponse or None if not found
        """
        # Validate path
        path = validate_secret_path(path)
        
        # Get existing secret
        query = select(SecretMetadata).where(
            and_(
                SecretMetadata.path == path,
                SecretMetadata.active == True
            )
        )
        result = await self.db.execute(query)
        secret = result.scalar_one_or_none()
        
        if not secret:
            return None
        
        # Check if value is being updated (creates new version)
        if data.value is not None:
            # Encrypt new value
            encrypted_value = self._encrypt(data.value)
            
            # Deactivate current version
            await self.db.execute(
                update(SecretVersion)
                .where(
                    and_(
                        SecretVersion.secret_id == secret.id,
                        SecretVersion.active == True
                    )
                )
                .values(active=False)
            )
            
            # Create new version
            new_version = SecretVersion(
                secret_id=secret.id,
                version=secret.current_version + 1,
                cipher_id=uuid4(),
                created_by=updated_by,
                creation_method='manual',
                active=True,
                metadata={'encrypted_value': encrypted_value}
            )
            
            self.db.add(new_version)
            secret.current_version += 1
        
        # Update other fields
        if data.description is not None:
            secret.description = data.description
        if data.tags is not None:
            secret.tags = data.tags
        if data.metadata is not None:
            secret.metadata = data.metadata
        if data.expires_at is not None:
            secret.expires_at = data.expires_at
        if data.active is not None:
            secret.active = data.active
        
        secret.updated_by = updated_by
        secret.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(secret)
        
        logger.info(
            "secret_updated",
            path=path,
            new_version=secret.current_version,
            updated_by=updated_by
        )
        
        # Return updated secret with value
        return await self.get_secret(path)
    
    async def delete_secret(
        self,
        path: str,
        hard_delete: bool = False
    ) -> bool:
        """
        Delete a secret (soft delete by default)
        
        Args:
            path: Secret path
            hard_delete: If True, permanently delete; else mark as inactive
            
        Returns:
            True if deleted, False if not found
        """
        # Validate path
        path = validate_secret_path(path)
        
        if hard_delete:
            # Permanently delete (cascades to versions)
            stmt = delete(SecretMetadata).where(SecretMetadata.path == path)
        else:
            # Soft delete (mark as inactive)
            stmt = (
                update(SecretMetadata)
                .where(SecretMetadata.path == path)
                .values(active=False)
            )
        
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        if result.rowcount > 0:
            logger.info(
                "secret_deleted",
                path=path,
                hard_delete=hard_delete
            )
            return True
        
        return False
    
    async def list_secrets(
        self,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        secret_type: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[SecretListItem], int]:
        """
        List secrets with filtering and pagination
        
        Args:
            prefix: Path prefix filter
            tags: Filter by tags (OR logic)
            secret_type: Filter by type
            page: Page number
            page_size: Results per page
            
        Returns:
            Tuple of (secrets list, total count)
        """
        # Build query
        query = select(SecretMetadata).where(SecretMetadata.active == True)
        
        # Apply filters
        if prefix:
            query = query.where(SecretMetadata.path.like(f"{prefix}%"))
        
        if tags:
            # PostgreSQL array overlap
            query = query.where(SecretMetadata.tags.overlap(tags))
        
        if secret_type:
            query = query.where(SecretMetadata.secret_type == secret_type)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        # Apply pagination and sorting
        query = query.offset((page - 1) * page_size).limit(page_size)
        query = query.order_by(SecretMetadata.path)
        
        result = await self.db.execute(query)
        secrets = result.scalars().all()
        
        # Convert to list items
        items = [
            SecretListItem(
                path=s.path,
                description=s.description,
                secret_type=s.secret_type,
                version=s.current_version,
                tags=s.tags,
                updated_at=s.updated_at,
                expires_at=s.expires_at
            )
            for s in secrets
        ]
        
        return items, total
    
    # ========================================================================
    # VERSION OPERATIONS
    # ========================================================================
    
    async def get_version_history(
        self,
        path: str
    ) -> Optional[List[SecretVersionResponse]]:
        """
        Get version history for a secret
        
        Args:
            path: Secret path
            
        Returns:
            List of SecretVersionResponse or None if not found
        """
        # Get secret
        secret = await self.get_secret_by_path(path, include_value=False)
        if not secret:
            return None
        
        # Get all versions
        query = select(SecretVersion).where(
            SecretVersion.secret_id == secret.id
        ).order_by(SecretVersion.version.desc())
        
        result = await self.db.execute(query)
        versions = result.scalars().all()
        
        return [
            SecretVersionResponse(
                id=v.id,
                secret_id=v.secret_id,
                version=v.version,
                created_at=v.created_at,
                created_by=v.created_by,
                creation_method=v.creation_method,
                active=v.active,
                metadata=v.metadata
            )
            for v in versions
        ]
    
    async def rollback_to_version(
        self,
        path: str,
        target_version: int,
        rolled_back_by: Optional[str] = None
    ) -> Optional[SecretResponse]:
        """
        Rollback secret to a previous version
        
        Args:
            path: Secret path
            target_version: Version to rollback to
            rolled_back_by: User performing rollback
            
        Returns:
            SecretResponse or None if not found
        """
        # Get secret
        secret = await self.get_secret_by_path(path, include_value=False)
        if not secret:
            return None
        
        # Get target version
        version_query = select(SecretVersion).where(
            and_(
                SecretVersion.secret_id == secret.id,
                SecretVersion.version == target_version
            )
        )
        result = await self.db.execute(version_query)
        target = result.scalar_one_or_none()
        
        if not target:
            raise ValueError(f"Version {target_version} not found")
        
        # Deactivate current version
        await self.db.execute(
            update(SecretVersion)
            .where(
                and_(
                    SecretVersion.secret_id == secret.id,
                    SecretVersion.active == True
                )
            )
            .values(active=False)
        )
        
        # Create new version (copy of target)
        encrypted_value = target.metadata.get('encrypted_value', '')
        
        new_version = SecretVersion(
            secret_id=secret.id,
            version=secret.current_version + 1,
            cipher_id=uuid4(),
            created_by=rolled_back_by,
            creation_method='rollback',
            active=True,
            metadata={
                'encrypted_value': encrypted_value,
                'rolled_back_from': target_version
            }
        )
        
        self.db.add(new_version)
        
        # Update secret
        await self.db.execute(
            update(SecretMetadata)
            .where(SecretMetadata.id == secret.id)
            .values(
                current_version=secret.current_version + 1,
                updated_by=rolled_back_by
            )
        )
        
        await self.db.commit()
        
        logger.info(
            "secret_rolled_back",
            path=path,
            target_version=target_version,
            new_version=secret.current_version + 1,
            rolled_back_by=rolled_back_by
        )
        
        return await self.get_secret(path)
    
    # ========================================================================
    # BATCH OPERATIONS
    # ========================================================================
    
    async def batch_get_secrets(
        self,
        paths: List[str]
    ) -> Dict[str, SecretResponse]:
        """
        Get multiple secrets at once
        
        Args:
            paths: List of secret paths
            
        Returns:
            Dict mapping path to SecretResponse
        """
        results = {}
        errors = {}
        
        for path in paths:
            try:
                secret = await self.get_secret(path)
                if secret:
                    results[path] = secret
                else:
                    errors[path] = "Secret not found"
            except Exception as e:
                errors[path] = str(e)
        
        return results, errors
    
    # ========================================================================
    # STATISTICS
    # ========================================================================
    
    async def get_statistics(self) -> SecretStatistics:
        """
        Get overall secret statistics
        
        Returns:
            SecretStatistics
        """
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        
        # Total secrets
        total = (await self.db.execute(
            select(func.count()).select_from(SecretMetadata)
            .where(SecretMetadata.active == True)
        )).scalar()
        
        # Active (non-expired)
        active = (await self.db.execute(
            select(func.count()).select_from(SecretMetadata)
            .where(
                and_(
                    SecretMetadata.active == True,
                    or_(
                        SecretMetadata.expires_at.is_(None),
                        SecretMetadata.expires_at > now
                    )
                )
            )
        )).scalar()
        
        # Expired
        expired = (await self.db.execute(
            select(func.count()).select_from(SecretMetadata)
            .where(
                and_(
                    SecretMetadata.active == True,
                    SecretMetadata.expires_at <= now
                )
            )
        )).scalar()
        
        # With rotation
        with_rotation = (await self.db.execute(
            select(func.count()).select_from(SecretMetadata)
            .where(
                and_(
                    SecretMetadata.active == True,
                    SecretMetadata.rotation_enabled == True
                )
            )
        )).scalar()
        
        # By type
        type_counts = {}
        # TODO: Implement type counting query
        
        # Total versions
        total_versions = (await self.db.execute(
            select(func.count()).select_from(SecretVersion)
        )).scalar()
        
        # Recent updates
        recent = (await self.db.execute(
            select(func.count()).select_from(SecretMetadata)
            .where(
                and_(
                    SecretMetadata.active == True,
                    SecretMetadata.updated_at >= yesterday
                )
            )
        )).scalar()
        
        avg_versions = total_versions / total if total > 0 else 0
        
        return SecretStatistics(
            total_secrets=total or 0,
            active_secrets=active or 0,
            expired_secrets=expired or 0,
            secrets_with_rotation=with_rotation or 0,
            secrets_by_type=type_counts,
            total_versions=total_versions or 0,
            average_versions_per_secret=round(avg_versions, 2),
            recent_updates_24h=recent or 0
        )

