from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

engine = create_async_engine(str(settings.POSTGRES_URL))
new_session = async_sessionmaker(engine, expire_on_commit=False)
    
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)
          