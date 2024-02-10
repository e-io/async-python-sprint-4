# for python 3.9
from __future__ import annotations

import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.base import RecordModel, UrlModel
from src.services.base import CRUD

from src.db.db import get_session


logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


router = APIRouter()

@router.post('/shorten/', status_code=201)
async def shorten_link(*, db: AsyncSession = Depends(get_session), link: UrlModel):
    """save link and return id"""
    logger.debug('link: %s', link.url)
    try:
        UrlModel(url=link.url)
    except ValidationError:
        raise HTTPException(status_code=422, detail='Input data is not a link')
    record: RecordModel = await CRUD.create_record(db=db, link=link)

    return record.json()


@router.get('/link', status_code=307)
async def return_link(*, db: AsyncSession = Depends(get_session), url_id: str):
    """return full link by id"""
    logger.debug('id: %s', url_id)
    record: RecordModel = await CRUD.read_record(db, url_id)
    logger.debug(record)
    url = record.url_full
    return {'url_full': url}


@router.get('/info')
async def info(*, db: AsyncSession = Depends(get_session), url_id: str):
    """info about one link"""
    logger.debug('id: %s', url_id)
    # /info does not increase the usage of link
    record: RecordModel = await CRUD.read_record(db, url_id, incr=False)
    return json.loads(record.json())


@router.patch('/deprecate', status_code=200)
async def deprecate(*, db: AsyncSession = Depends(get_session), url_id: str):
    """to deprecate (or "delete") a link"""
    await CRUD.deprecate_record(db, url_id)
    return {}


@router.post('/shorten-batch')
async def shorten_links():
    """batch upload - save many link and return their ids"""
    ...
    return {'response': 'Not implemented'}


@router.get('/ping')
async def ping(*, db: AsyncSession = Depends(get_session)):
    return {'Is database available': False}


@router.get('/hello')  # hello world
async def hello_world():
    return {'hello': 'world'}


@router.get('/{action}')
async def handler_other(action):
    return {'next page is asked but it does not exist': action}
