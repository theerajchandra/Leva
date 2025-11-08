# /app/db/session.py
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/leva")

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a sessionmaker
# expire_on_commit=False is important for using models after commit in async code
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Our models will inherit from this class
Base = declarative_base()

# Dependency to get a DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get an async database session.
    """
    async with async_session() as session:
        yield session
