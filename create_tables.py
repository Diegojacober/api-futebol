from core.configs import settings
from core.database import engine

async def create_tables() -> None:
    import models.__all_models
    print('Creating...')
    
    async with engine.begin() as conn:
        await conn.run_sync(settings.DB_BASEMODEL.metadata.drop_all)
        await conn.run_sync(settings.DB_BASEMODEL.metadata.create_all)
        print('Created with success!!')
            
if __name__ == '__main__':
    import asyncio
    
    asyncio.run(create_tables())