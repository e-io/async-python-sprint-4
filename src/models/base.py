from pydantic import BaseModel, HttpUrl, ValidationError

class UrlModel(BaseModel):
    url: HttpUrl
