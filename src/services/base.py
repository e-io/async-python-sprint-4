from __future__ import annotations

import asyncio
from hashlib import sha256
import sqlalchemy

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.base import LENGTH, IdModel, RecordModel, UrlModel
import logging

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class DB:
    data: dict = {}


class CRUD:
    @staticmethod
    async def _all_ids(db: AsyncSession):
        statement = select([RecordModel.url_id])
        all_ids_iterator = await db.execute(statement=statement)
        all_ids = all_ids_iterator.all()
        return all_ids

    @staticmethod
    async def _create_id(string: str):
        return sha256(string.encode()).hexdigest()[0:LENGTH]

    @staticmethod
    async def create_record(db: AsyncSession, link: UrlModel | str):
        # id is a short link
        url = link.url if isinstance(link, UrlModel) else link
        id = await CRUD._create_id(url)
        MAX_ATTEMPTS = 128
        count = MAX_ATTEMPTS

        while id in await CRUD._all_ids(db=db):
            id = await CRUD._create_id(id)
            count -= 1
            if count == 0:
                raise HTTPException(
                    status_code=500,
                    detail='Server could not create a hashsum for a short link',
                )

        http_url = UrlModel(url=url)
        record = RecordModel(url_id=id, url_full=http_url.url, used=0, deprecated=False)

        db.add(record)
        await db.commit()
        await asyncio.sleep(0.25)

        record_read = await CRUD._read_record(db, id)

        return record_read

    @staticmethod
    async def _read_record(db: AsyncSession, id_: IdModel | str) -> RecordModel:
        # just a simple read from database WITHOUT any checks
        statement = select(RecordModel).where(RecordModel.url_id == id_)
        rows = await db.execute(statement)
        row: sqlalchemy.engine.row.Row = rows.first()
        assert isinstance(row, sqlalchemy.engine.row.Row)
        record = row['RecordModel']
        logger.debug(record.json())
        return record

    @staticmethod
    async def read_record(db: AsyncSession, id_: IdModel | str, incr=True):
        """
        incr: in the most cases we increment
        the number of usage of the link
        """

        if id_ not in await CRUD._all_ids(db=db):
            raise HTTPException(
                status_code=404, detail=f'There is no a link with this id {id_}'
            )

        async with db as session:
            statement = select(RecordModel).where(RecordModel.url_id == id_)
            records = await session.execute(statement)
            record = records.first()
            print('line 75 ', record)

            print('l87 all_ids:', await CRUD._all_ids_future(db=db))

        record = DB.data[id_]

        if record.deprecated is True:
            raise HTTPException(
                status_code=410,
                detail=f'Gone. This short link {id_} is deprecated forever',
            )
        # it's needed to update `used` in a database
        if incr:
            DB.data[id_].used += 1

        return DB.data[id_]

    @staticmethod
    async def deprecate_record(db: AsyncSession, id_: IdModel | str):
        if id_ not in await CRUD._all_ids(db=db):
            raise HTTPException(
                status_code=404, detail=f'There is no a link with this id {id_}'
            )

        DB.data[id_].deprecated = True

        return DB.data[id_]
