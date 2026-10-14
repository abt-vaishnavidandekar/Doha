import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"))

AsyncSessionLocal = async_sessionmaker(engine, class_= AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session