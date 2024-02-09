from pydantic import BaseModel, Field, HttpUrl

LENGTH = 4


class UrlModel(BaseModel):
    url: HttpUrl


class IdModel(BaseModel):
    id: str = Field(min_length=LENGTH, max_length=LENGTH)


class RecordModel(BaseModel):
    """entity model for "database"""

    url_id: str = Field(min_length=LENGTH, max_length=LENGTH)
    url_full: HttpUrl
    used: int = 0  # how many times this link was used
    deprecated: bool = False
