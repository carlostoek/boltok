import asyncio
import asyncpg
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_connection():
    connection_url = "postgresql+asyncpg://postgres:jXzMGzumFLnmWFTOGyUDNIUHJZpcEbVB@postgres.railway.internal:5432/railway"
    
    try:
        # Extract connection parameters
        parts = connection_url.split('://')[1].split('@')
        credentials, hostport = parts[0].split(':'), parts[1].split(':')
        user, password = credentials[0], credentials[1]
        host, port = hostport[0], hostport[1].split('/')[0]
        database = hostport[1].split('/')[1]
        
        logger.info("Testing PostgreSQL connection...")
        logger.info(f"Host: {host}, Port: {port}, Database: {database}")
        
        # Attempt connection
        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=database,
            host=host,
            port=int(port),
            timeout=10
        )
        
        version = await conn.fetchval('SELECT version()')
        await conn.close()
        
        logger.info(f"✅ Connection successful! PostgreSQL version: {version}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == '__main__':
    asyncio.run(test_connection())
