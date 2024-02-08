from hashlib import sha256

from fastapi import HTTPException

from src.models.base import LENGTH, IdModel, RecordModel, UrlModel


class DB:
    data: dict = {}


class CRUD:
    @staticmethod
    def _create_id(string: str):
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

    @staticmethod
    def read_record(id_: IdModel, incr=True):
        """
        incr: in the most cases we increment
        the number of usage of the link
        """
        if id_ not in DB.data:
            return HTTPException(status_code=404, detail=f'There is no a link with this id {id_}')

        if incr:
            DB.data[id_].used += 1

        return DB.data[id_]
