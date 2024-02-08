from hashlib import sha256

from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl

from src.models.base import UrlModel, RecordModel


class DB:
    data: dict = {}


class CRUD:
    @staticmethod
    def _create_id(string: str):
        LENGTH = 3
        return sha256(string.encode()).hexdigest()[0:LENGTH]


    @staticmethod
    def create_Record(link: UrlModel):
        # id is a short link
        id = CRUD._create_id(link.url)
        MAX_ATTEMPTS = 128
        count = MAX_ATTEMPTS
        while id in DB.data.keys():
            id = CRUD._create_id(id)
            count -= 1
            if count == 0:
                raise HTTPException(
                    status_code=500, detail='Server could not create a hashsum for a short link'
                )
        record = RecordModel(url_id=id, url_full=link.url, used=0, deleted=False)
        DB.data[id] = record

        return DB.data[id]
