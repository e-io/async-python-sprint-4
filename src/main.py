"""
Run through console:

uvicorn src.main:app --host 127.0.0.1 --port 8080
additional notes are in the `../README.md` file

Routs which work "from the box":

docs_url: "/docs" - Swagger
redoc_url: "/redoc" - ReDoc
openapi_url: "/openapi.json" - OpenAPI documentation
"""
from fastapi import FastAPI

from src.apiv1 import base as apiv1_base
from src.core import config

def get_application():
    _app = FastAPI(
        title=config.app_settings.PROJECT_NAME,
    )
    _app.include_router(apiv1_base.router, prefix='')

    return _app


app = get_application()
