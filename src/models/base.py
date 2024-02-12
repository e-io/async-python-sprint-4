from pydantic import BaseModel, HttpUrl
from sqlmodel import Field, SQLModel

LENGTH = 4


class UrlModel(BaseModel):
    """To check that urls are valid. Not a random string."""

    url: HttpUrl


class IdModel(BaseModel):
    """To check just a length of string."""

    id: str = Field(min_length=LENGTH, max_length=LENGTH)


class RecordModel(SQLModel, table=True):
    """entity model for a database"""

    url_id: str = Field(min_length=LENGTH, max_length=LENGTH, primary_key=True)
    url_full: HttpUrl
    used: int = 0  # how many times this link was used
    deprecated: bool = False
