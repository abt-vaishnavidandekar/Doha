from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.configs.env import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(engine, class_= AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session