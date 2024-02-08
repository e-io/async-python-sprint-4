from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from src.models.base import UrlModel, RecordModel
from src.services.base import CRUD

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


router = APIRouter()


@router.post('/shorten/')
async def shorten_link(link: UrlModel):
    """save link and return id"""
    logger.debug('link: %s', link.url)
    try:
        UrlModel(url=link.url)
    except ValidationError:
        raise HTTPException(status_code=422, detail="Input data is not a link")
    record: RecordModel = CRUD.create_Record(link=link)

    return record.json()


@router.post('/shorten-batch')
async def shorten_links():
    """batch upload - save many link and return their ids"""
    ...
    return {'response': 'Not implemented'}


@router.get('/link')
async def return_link(id: str):
    """return full link by id"""
    ...
    return {'response': 'Not implemented'}


@router.get('/info')
async def info(id: str):
    """info about one link"""
    ...
    return {'response': 'Not implemented'}


@router.get('/all')
async def return_all_links():
    """return info about all links (just for debugging)"""
    ...
    return {'response': 'Not implemented'}


@router.get('/ping')
async def ping():
    return {'Is database available': False}


@router.get('/hello')  # hello world
async def hello_world():
    return {'hello': 'world'}


@router.get('/{action}')
async def handler_other(action):
    return {'next page is asked but it does not exist': action}
