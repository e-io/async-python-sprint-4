import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
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


