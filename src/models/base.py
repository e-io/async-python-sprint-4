from pydantic import BaseModel, HttpUrl, ValidationError


class UrlModel(BaseModel):
    url: HttpUrl


class RecordModel(BaseModel):
    """entity model for "database"""
    url_id: str
    url_full: HttpUrl
    used: int = 0  # how many times this link was used
    deleted: bool = False
