"""
Database Configuration

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05

SQLAlchemy async database configuration
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import structlog

from config.settings import get_settings

settings = get_settings()
logger = structlog.get_logger()


# ============================================================================
# DATABASE ENGINE
# ============================================================================

# Convert postgresql:// to postgresql+asyncpg://
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    database_url,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ============================================================================
# DATABASE SESSION DEPENDENCY
# ============================================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions
    
    Usage:
        @app.get("/example")
        async def example(db: AsyncSession = Depends(get_db)):
            # Use db here
            pass
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(
                "database_session_error",
                error=str(e),
                exc_info=True
            )
            await session.rollback()
            raise
        finally:
            await session.close()


# ============================================================================
# DATABASE UTILITIES
# ============================================================================

async def init_db():
    """
    Initialize database (create tables if they don't exist)
    
    Note: In production, use migrations instead (Alembic)
    """
    from database.models import Base
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("database_initialized", message="All tables created")


async def close_db():
    """Close database connections"""
    await engine.dispose()
    logger.info("database_closed", message="Database connections closed")


@asynccontextmanager
async def get_db_context():
    """
    Context manager for database sessions (useful for scripts)
    
    Usage:
        async with get_db_context() as db:
            # Use db here
            pass
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(
                "database_context_error",
                error=str(e),
                exc_info=True
            )
            raise
        finally:
            await session.close()


async def check_db_connection() -> bool:
    """
    Check if database connection is working
    
    Returns:
        bool: True if connection is successful
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error(
            "database_connection_check_failed",
            error=str(e)
        )
        return False


# ============================================================================
# TRANSACTION UTILITIES
# ============================================================================

@asynccontextmanager
async def transaction(db: AsyncSession):
    """
    Transaction context manager
    
    Usage:
        async with transaction(db):
            # All operations here are in a transaction
            # Automatically commits on success, rolls back on error
            pass
    
    Args:
        db: AsyncSession instance
    """
    async with db.begin():
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
        else:
            await db.commit()

