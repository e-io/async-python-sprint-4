import json
import logging
from asyncio import sleep

import httpx
from httpx import AsyncClient
from pytest import fixture, mark

client = AsyncClient(base_url='http://127.0.0.1:8080/')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@fixture
def url_example():
    return 'https://example.com/info?key=true&list=10'


@fixture
def url_examples():
    _urls = [
        'https://example.com/contacts',
        'http://example.com/a/b',
        'https://example.com/info?key=true&list=10',
    ]
    return _urls


@fixture
def not_urls():
    _not_urls = [
        'a',
        '',
        'Luke, I am your father',
        'htp://example.com',
        'http://example',
        'http://example .com',
    ]
    return _not_urls


@mark.asyncio
async def test_get_hello():
    response = await client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}


async def test_get_abracadabra():
    response = await client.get('/abracadabra')
    assert response.status_code == 200
    assert response.json() == {
        'next page is asked but it does not exist': 'abracadabra'
    }


@mark.asyncio
async def test_post_url(url_examples):
    for url_example in url_examples:
        logger.debug('URL example: %s', url_example)
        response = await client.post('/shorten/', headers={}, json={'url': url_example})
        await sleep(1)
        assert response.status_code == 201
        record = response.json()  # dict

        logger.debug(type(record))  # dict
        logger.debug(record)

        assert record['url_full'] == url_example
        assert 'url_id' in record
        assert isinstance(record['used'], int)
        assert record['deprecated'] is False


@mark.asyncio
async def test_post_not_urls(not_urls):
    for not_url in not_urls:
        response = await client.post('/shorten/', headers={}, json={'url': not_url})

        assert isinstance(response, httpx.Response)
        assert response.status_code == 422

        response_dict = json.loads(response.text)
        response_dict = response_dict['detail'][0]
        # responses have extremely good description of error
        logger.debug('%s%s%s', response_dict['type'], ': ', response_dict['msg'])


@mark.asyncio
async def test_post_and_get(url_example):
    response = await client.post('/shorten/', headers={}, json={'url': url_example})

    assert response.status_code == 201
    record = response.json()

    assert record['url_full'] == url_example
    url_id = record['url_id']
    logger.debug('url_id: %s', url_id)

    route = '/link' + '?url_id=' + url_id
    logger.debug('get route %s', route)

    response = await client.get(route)
    assert response.status_code == 307
    url_dict = response.json()
    url_full = url_dict['url_full']
    logger.debug('test got back url - %s', url_full)
    assert url_full == url_example


@mark.asyncio
async def test_info(url_example):
    response = await client.post('/shorten/', headers={}, json={'url': url_example})
    assert response.status_code == 201
    record = response.json()
    url_id = record['url_id']

    route = '/info' + '?url_id=' + url_id
    logger.debug('get route %s', route)
    response = await client.get(route)
    assert response.status_code == 200
    record_dict = response.json()
    assert record_dict['url_full'] == url_example
    logger.debug('test got json %s', record_dict)
    assert record_dict['deprecated'] is False
    assert record_dict['used'] == 0
    assert record_dict['url_id'] == url_id


@mark.asyncio
async def test_deprecated(url_example):
    response = await client.post('/shorten/', headers={}, json={'url': url_example})
    assert response.status_code == 201
    record = response.json()
    url_id = record['url_id']

    route = '/deprecate' + '?url_id=' + url_id
    response = await client.patch(route)
    assert response.status_code == 200

    route = '/link' + '?url_id=' + url_id
    response = await client.get(route)
    # '410' should be for a deprecated link. not 200.
    assert response.status_code == 410
