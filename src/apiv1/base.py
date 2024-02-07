from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post('/shorten')
async def shorten_link():
    """save link and return id"""
    ...
    return {'response': 'Not implemented'}

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
