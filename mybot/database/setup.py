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
    'narrative_choices', 
    'user_narrative_states',
    'rewards',
    'lore_pieces',
    'missions',
    'events',
    'raffles',
    'badges',
    'levels',
    'invite_tokens',
    'subscription_plans',
    'subscription_tokens',
    'tariffs',
    'config_entries',
    'bot_config',
    'channels',
    'pending_channel_requests',
    'challenges',
    'auctions',
    'trivias',
    'user_rewards',
    'user_achievements',
    'user_mission_entries',
    'raffle_entries',
    'user_badges',
    'vip_subscriptions',
    'user_stats',
    'tokens',
    'user_challenge_progress',
    'button_reactions',
    'bids',
    'auction_participants',
    'minigame_play',
    'user_lore_pieces',
    'trivia_questions',
    'trivia_attempts',
    'trivia_user_answers',
]

async def init_db():
    global _engine
    try:
        logger.info("Creando motor de base de datos...")
        
        # Verificar y corregir DATABASE_URL si es necesario
        db_url = Config.DATABASE_URL
        if db_url.startswith("postgres"):
            logger.warning("PostgreSQL detectado pero no disponible, cambiando a SQLite")
            db_url = "sqlite+aiosqlite:///gamification.db"
            
        if _engine is None:
            _engine = create_async_engine(
                db_url, 
                echo=False, 
                poolclass=NullPool
            )
        
        async with _engine.begin() as conn:
            # Verificar qué tablas ya existen
            inspector = inspect(await conn.get_sync_connection())
            existing_tables = inspector.get_table_names()
            
            # Filtrar solo las tablas que necesitamos crear
            tables_to_create = [
                table for table in TABLES_ORDER 
                if table not in existing_tables
            ]
            
            if tables_to_create:
                logger.info(f"Creando tablas: {', '.join(tables_to_create)}")
                tables = [Base.metadata.tables[name] for name in tables_to_create]
                await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=tables))
                logger.info(f"Tablas creadas exitosamente: {', '.join(tables_to_create)}")
            else:
                logger.info("Todas las tablas ya existen, no se requiere creación")
                
        return _engine
    except Exception as e:
        logger.critical(f"Error crítico en init_db: {str(e)}")
        raise

def get_session_factory():
    global _sessionmaker
    if _engine is None:
        raise RuntimeError("Database engine not initialized. Call init_db first.")
    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(
            bind=_engine, 
            expire_on_commit=False,
            class_=AsyncSession
        )
    return _sessionmaker

async def get_session() -> AsyncSession:
    session_factory = get_session_factory()
    return session_factory()
