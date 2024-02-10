from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, SQLModel

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
