import logging
from time import sleep

from fastapi.testclient import TestClient
from pytest import fixture

from main import app

client = TestClient(app)
logging.basicConfig(level='DEBUG')


@fixture
def url_example():
    return 'https://example.com'


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


def test_post_link(url_example):
    logging.debug('URL example: %s', url_example)
    response = client.post('/shorten/', headers={}, json={'url': url_example})
    sleep(1)
    assert response.status_code == 200
    json_ = response.json()
    assert json_['link'] == url_example  #
    # assert 'url_id' in json_
