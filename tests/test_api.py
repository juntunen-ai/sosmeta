import os
import sys
import pytest

os.environ['API_KEY'] = 'testkey'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server_example import app

app.config['TESTING'] = True

@pytest.fixture

def client():
    with app.test_client() as client:
        yield client

def auth_header():
    return {'Authorization': 'Bearer testkey'}

def test_health(client, auth_header):
    resp = client.get('/health', headers=auth_header())
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'healthy'
    assert 'schemas_loaded' in data
    assert 'timestamp' in data

def test_list_schemas(client, auth_header):
    resp = client.get('/api/v1/schemas', headers=auth_header())
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data['schemas'], list)


def test_validate_invalid(client, auth_header):
    payload = {
        'schemaOid': '1.2.246.537.6.1506.1000.2023.9.8',
        'document': {}
    }
    resp = client.post('/api/v1/validate', json=payload, headers=auth_header())
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['valid'] is False
    assert 'errors' in data

