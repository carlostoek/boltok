import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram bot configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
if BOT_TOKEN == "YOUR_BOT_TOKEN" or not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set or contains the default placeholder.")

ADMIN_IDS: List[int] = [
    int(uid) for uid in os.environ.get("ADMIN_IDS", "").split(";") if uid.strip()
]

VIP_CHANNEL_ID = int(os.environ.get("VIP_CHANNEL_ID", "0"))
FREE_CHANNEL_ID = int(os.environ.get("FREE_CHANNEL_ID", "0"))

# Scheduler intervals
CHANNEL_SCHEDULER_INTERVAL = int(os.environ.get("CHANNEL_SCHEDULER_INTERVAL", "30"))
VIP_SCHEDULER_INTERVAL = int(os.environ.get("VIP_SCHEDULER_INTERVAL", "3600"))

# Default reaction buttons
DEFAULT_REACTION_BUTTONS = ["👍", "❤️", "😂", "🔥", "💯"]

class Config:
    BOT_TOKEN = BOT_TOKEN
    ADMIN_ID = ADMIN_IDS[0] if ADMIN_IDS else 0
    CHANNEL_ID = VIP_CHANNEL_ID
    FREE_CHANNEL_ID = FREE_CHANNEL_ID
    
    # Configuración PostgreSQL (requiere variables de entorno)
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "gamification_bot")
    
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    CHANNEL_SCHEDULER_INTERVAL = CHANNEL_SCHEDULER_INTERVAL
    VIP_SCHEDULER_INTERVAL = VIP_SCHEDULER_INTERVAL
