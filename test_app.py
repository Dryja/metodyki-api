import pytest

from app import api, application


@pytest.fixture
def test_client():
    application.config['TESTING'] = True
    test_client = api.app.test_client()

    yield test_client


def test_valid_operations(test_client):
    """
    GIVEN a Flask API
    WHEN access the '/operations' endpoint (POST) 
    THEN check the response is valid
    """
    response = test_client.post('/operations',
                                json={'operation': '(1,23e+10 - 3) * 5 = 6,15e+10'})

    assert response.status_code == 201
    assert b'' in response.data

    """
    GIVEN a Flask API
    WHEN access the '/operations' endpoint (GET)
    THEN check the response is valid
    """
    response = test_client.get('/operations')

    assert response.status_code == 200
    assert b'(1,23e+10 - 3) * 5 = 6,15e+10' in response.data

    """
    GIVEN a FLASK API
    WHEN access the '/operations' endpoint (DELETE)
    THEN check the response is valid
    """
    response = test_client.delete('/operations')

    assert response.status_code == 200
    assert b'' in response.data


def test_invalid_operations(test_client):
    """
    GIVEN a Flask API
    WHEN access the '/operations' endpoint (POST)
    THEN check the response is invalid
    """
    response = test_client.post('/operations',
                                json={})

    assert response.status_code == 400
    assert b'' in response.data


def test_valid_color(test_client):
    """
    GIVEN a FLASK API
    WHEN access the '/color' endpoint (GET)
    THEN check the response is valid
    """
    response = test_client.get('/color')

    assert response.status_code == 200
    assert b'color' in response.data
