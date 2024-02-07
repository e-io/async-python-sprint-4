from pydantic import BaseModel


class URL(BaseModel):
    url_id: str
    url_full: str
    used: int  # how many times this link was used
    deleted: bool


class DB:
    data: dict = {}
