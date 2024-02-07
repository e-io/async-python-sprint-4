from hashlib import sha256

from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl

from src.models.base import UrlModel


class URL(BaseModel):
    url_id: str
    url_full: HttpUrl
    used: int = 0  # how many times this link was used
    deleted: bool = False


class DB:
    data: dict = {}


class CRUD:
    @staticmethod
    def create_URL(link: UrlModel):
        # id is a short link
        id = sha256(link.url.encode()).hexdigest()[0:6]
        count = 100
        while id in DB.data.keys():
            id = sha256(id.encode()).hexdigest()[0:6]
            count -= 1
            if count == 0:
                raise HTTPException(
                    status_code=500, detail='Server could not create a hashsum'
                )
        url = URL(url_id=id, url_full=link.url, used=0, deleted=False)
        DB.data[id] = url

        return DB.data[id]
