import os
import datetime

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column, Mapped
from sqlalchemy import func


POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

POSTGRES_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_async_engine(POSTGRES_DSN)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Character(Base):
    __tablename__ = "items"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    api_id: MappedColumn[int] = mapped_column(Integer)
    name: MappedColumn[str] = MappedColumn(String, unique=True)
    birth_year: MappedColumn[str] = mapped_column(String)
    eye_color: MappedColumn[str] = mapped_column(String)
    gender: MappedColumn[str] = mapped_column(String)
    hair_color: MappedColumn[str] = mapped_column(String)
    homeworld: MappedColumn[str] = mapped_column(String)
    mass: MappedColumn[str] = mapped_column(String)
    skin_color: MappedColumn[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()