import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import SQLModel


async def prepare_engine(dsn: str, echo=False):
    engine = create_async_engine(
        dsn,
        echo=echo,
        future=True,
    )

    # init models
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    return engine

async def prepare_session(dsn: str, echo=False):
    engine = await prepare_engine(dsn, echo)
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return async_session


async def get_session() -> AsyncSession:
    dsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

    async_session = await prepare_session(dsn=dsn, echo=False)

    async with async_session() as session:
        yield session
