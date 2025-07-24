# database/setup.py
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import inspect
from .base import Base
from utils.config import Config

logger = logging.getLogger(__name__)

_engine = None
_sessionmaker = None

async def init_db():
    global _engine, _sessionmaker
    try:
        logger.info("Inicializando conexión a PostgreSQL...")
        
        _engine = create_async_engine(
            Config.DATABASE_URL,
            echo=True,
            pool_size=20,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600
        )
        
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tablas creadas exitosamente")
            
        _sessionmaker = async_sessionmaker(
            bind=_engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        
        return _engine
    except Exception as e:
        logger.critical(f"Error al conectar con PostgreSQL: {str(e)}")
        raise

def get_session_factory():
    if not _sessionmaker:
        raise RuntimeError("Debes llamar a init_db() primero")
    return _sessionmaker

async def close_db():
    global _engine, _sessionmaker
    if _engine:
        await _engine.dispose()
        _engine = None
        _sessionmaker = None
        logger.info("Conexión a PostgreSQL cerrada")
