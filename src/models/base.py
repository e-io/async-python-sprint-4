from pydantic import BaseModel, HttpUrl
from sqlmodel import SQLModel, Field

LENGTH = 4


class UrlModel(BaseModel):
    url: HttpUrl


class IdModel(BaseModel):
    id: str = Field(min_length=LENGTH, max_length=LENGTH)


class RecordModel(SQLModel, table=True):
    """entity model for "database"""

    url_id: str = Field(min_length=LENGTH, max_length=LENGTH, primary_key=True)
    url_full: HttpUrl
    used: int = 0  # how many times this link was used
    deprecated: bool = False


import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db import prepare_engine

async def function_example():
    dsn = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

    engine = await prepare_engine(dsn=dsn, echo=False)

    record1 = RecordModel(url_id='abcd', url_full='https://example.com')
    record2 = RecordModel(url_id='1234', url_full='https://example.com/info?key=true&list=10')

    async with AsyncSession(engine) as session:
        session.add(record1)
        session.add(record2)

        await session.commit()

    await asyncio.sleep(1)

    url_id1 = 'abcd'
    async with AsyncSession(engine) as session:
        statement = select(RecordModel).where(RecordModel.url_id == url_id1)
        records = await session.execute(statement)
        record = records.first()
        print(record)


if __name__ == '__main__':
    asyncio.run(function_example())
