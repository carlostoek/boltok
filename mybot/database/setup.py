import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import inspect, text
from .base import Base
from utils.config import Config

logger = logging.getLogger(__name__)

_engine = None
_sessionmaker = None

async def init_db():
    global _engine, _sessionmaker
    try:
        logger.info("Initializing PostgreSQL connection with SQLAlchemy...")
        
        # CRITICAL FIX: Use NullPool for Railway environment
        _engine = create_async_engine(
            Config.DATABASE_URL,
            echo=True,
            poolclass=NullPool,  # Essential for Railway's connection handling
            connect_args={
                "timeout": 10,  # Match our successful test
                "server_settings": {
                    "application_name": "gamification-bot"
                }
            }
        )
        
        # Verify connection
        async with _engine.connect() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            logger.info(f"✅ SQLAlchemy connected to PostgreSQL {version}")
        
        # Create tables
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully")
            
        _sessionmaker = async_sessionmaker(
            bind=_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False  # Prevent premature flushes
        )
        
        return _engine
    except Exception as e:
        logger.critical(f"SQLAlchemy connection failed: {str(e)}")
        raise

def get_session_factory():
    if not _sessionmaker:
        raise RuntimeError("Call init_db() first")
    return _sessionmaker

async def close_db():
    global _engine, _sessionmaker
    if _engine:
        await _engine.dispose()
        _engine = None
        _sessionmaker = None
        logger.info("PostgreSQL connection closed")
