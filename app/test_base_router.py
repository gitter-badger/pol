from starlette.testclient import TestClient


def test_doc_html(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']


def test_openapi_json(client: TestClient):
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'


def test_deprecated_calendar(client: TestClient):
    response = client.get('/calendar/any-auth')
    assert response.status_code == 200
    assert response.text


def test_bgm_tv_user_calendar(client: TestClient):
    response = client.get('/api.v1/calendar/bgm.tv/1')
    assert 'text/calendar' in response.headers['content-type']
