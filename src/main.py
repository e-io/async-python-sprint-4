"""
Routs which work "from the box":

docs_url: "/docs" - Swagger
redoc_url: "/redoc" - ReDoc
openapi_url: "/openapi.json" - OpenAPI documentation
"""
from fastapi import FastAPI

from src.core import config


def get_application():
    _app = FastAPI(
        title=config.app_settings.PROJECT_NAME,
    )

    return _app


app = get_application()
