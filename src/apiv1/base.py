from __future__ import annotations

import json
import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from src.models.base import RecordModel, UrlModel
from src.services.base import CRUD

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


router = APIRouter()


@router.post('/shorten/', status_code=201)
async def shorten_link(link: UrlModel):
    """save link and return id"""
    logger.debug('link: %s', link.url)
    try:
        UrlModel(url=link.url)
    except ValidationError:
        raise HTTPException(status_code=422, detail='Input data is not a link')
    record: RecordModel = CRUD.create_record(link=link)

    return record.json()


@router.post('/shorten-batch')
async def shorten_links():
    """batch upload - save many link and return their ids"""
    ...
    return {'response': 'Not implemented'}


@router.get('/link', status_code=307)
async def return_link(url_id: str):
    """return full link by id"""
    logger.debug('id: %s', url_id)
    record: RecordModel = CRUD.read_record(url_id)
    logger.debug(record)
    url = record.url_full
    return {'url_full': url}


@router.get('/info')
async def info(url_id: str):
    """info about one link"""
    logger.debug('id: %s', url_id)
    # /info does not increase the usage of link
    record: RecordModel = CRUD.read_record(url_id, incr=False)
    return json.loads(record.json())


@router.patch('/deprecate', status_code=200)
async def deprecate(url_id: str):
    """to deprecate (or "delete") a link"""
    record: RecordModel = CRUD.deprecate_record(url_id)
    return {}


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
