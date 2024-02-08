import logging
import json
from time import sleep
import requests

from fastapi.testclient import TestClient
from pytest import fixture

from main import app

client = TestClient(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


@fixture
def url_example():
    return 'https://example.com'

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


def test_get_hello():
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}


def test_get_abracadabra():
    response = client.get('/abracadabra')
    assert response.status_code == 200
    assert response.json() == {
        'next page is asked but it does not exist': 'abracadabra'
    }


def test_post_url(url_example):
    logger.debug('URL example: %s', url_example)
    response = client.post('/shorten/', headers={}, json={'url': url_example})
    sleep(1)
    assert response.status_code == 201
    record_as_string = response.json()  # response.json() has a type <str>! (not dict)
    record = json.loads(record_as_string)
    logger.debug(type(record))  # dict
    logger.debug(record)

    assert record['url_full'] == url_example
    assert 'url_id' in record
    assert isinstance(record['used'], int)
    assert record['deprecated'] is False


def test_post_not_urls(not_urls):
    for not_url in not_urls:
        response = client.post('/shorten/', headers={}, json={'url': not_url})

        # is not true for the last libraries OR python 3.11
        # assert isinstance(response, requests.models.Response)
        assert response.status_code == 422

        response_dict = json.loads(response.text)
        response_dict = response_dict['detail'][0]
        # responses have extremely good description of error
        logger.debug('%s%s%s', response_dict['type'], ': ', response_dict['msg'])


def test_post_and_get(url_example):
    response = client.post('/shorten/', headers={}, json={'url': url_example})

    assert response.status_code == 201
    record_as_string = response.json()  # response.json() has a type <str>! (not dict)
    record = json.loads(record_as_string)

    assert record['url_full'] == url_example
    url_id = record['url_id']
    logger.debug('url_id: %s', url_id)

    route = '/link' + '?url_id=' + url_id
    logger.debug('get route %s', route)
    response = client.get(route)
    assert response.status_code == 307
    url_dict = response.json()
    url_full = url_dict['url_full']
    logger.debug('test got back url - %s', url_full)
    assert url_full == url_example

def test_info(url_example):
    response = client.post('/shorten/', headers={}, json={'url': url_example})
    assert response.status_code == 201
    record_as_string = response.json()  # response.json() has a type <str>! (not dict)
    record = json.loads(record_as_string)
    url_id = record['url_id']

    route = '/info' + '?url_id=' + url_id
    logger.debug('get route %s', route)
    response = client.get(route)
    assert response.status_code == 200
    record_dict = response.json()
    assert record_dict['url_full'] == url_example
    logger.debug('test got json %s', record_dict)
    assert record_dict['deprecated'] == False
    assert record_dict['used'] == 0
    assert record_dict['url_id'] == url_id

def test_deprecated(url_example):
    response = client.post('/shorten/', headers={}, json={'url': url_example})
    assert response.status_code == 201
    record_as_string = response.json()  # response.json() has a type <str>! (not dict)
    record = json.loads(record_as_string)
    url_id = record['url_id']

    route = '/deprecate' + '?url_id=' + url_id
    response = client.patch(route)
    assert response.status_code == 200

    route = '/link' + '?url_id=' + url_id
    response = client.get(route)
    assert response.status_code == 410  # as it should be
