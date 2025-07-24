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

TABLES_ORDER = [
    'users',
    'achievements',
    'story_fragments',
    # ... (resto de tablas permanece igual)
]

async def init_db():
    global _engine
    try:
        logger.info("Inicializando conexión a PostgreSQL...")
        
        if _engine is None:
            _engine = create_async_engine(
                Config.DATABASE_URL,
                echo=True,  # Habilitar para debugging
                pool_size=20,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600
            )
        
        async with _engine.begin() as conn:
            # Verificar conexión
            await conn.execute("SELECT 1")
            logger.info("Conexión a PostgreSQL establecida correctamente")
            
            # Verificar qué tablas ya existen
            inspector = inspect(await conn.get_sync_connection())
            existing_tables = inspector.get_table_names()
            
            tables_to_create = [
                table for table in TABLES_ORDER 
                if table not in existing_tables
            ]
            
            if tables_to_create:
                logger.info(f"Creando tablas faltantes: {', '.join(tables_to_create)}")
                tables = [Base.metadata.tables[name] for name in tables_to_create]
                await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=tables))
                logger.info("Tablas creadas exitosamente")
            else:
                logger.info("Todas las tablas ya existen en PostgreSQL")
                
        return _engine
    except Exception as e:
        logger.critical(f"Error al conectar con PostgreSQL: {str(e)}")
        raise

# ... (resto del código permanece igual)
