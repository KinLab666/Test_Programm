import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_task(client):
    response = client.post('/tasks', json={
        "title": "Тестовая задача",
        "description": "описание",
        "tags": ["тест"]
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Тестовая задача"

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200

def test_get_task(client):
    response = client.get('/tasks/1')
    assert response.status_code == 200

def test_update_task(client):
    response = client.put('/tasks/1', json={
        "title": "Тестовая задача измененная",
        "description": "описание изменено",
        "tags": ["изменено"]
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Тестовая задача измененная"

def test_delete_task(client):
    response = client.delete('/tasks/1')
    assert response.status_code == 200

def test_create_tag(client):
    response = client.post('/tags', json={"name": "Тестовый"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == "Тестовый"

def test_update_tag(client):
    response = client.put('/tags', json={"name": "измененная"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == "измененная"

def test_get_tags(client):
    response = client.get('/tags')
    assert response.status_code == 200

def test_get_tag(client):
    response = client.get('/tags/1')
    assert response.status_code == 200

def test_delete_tag(client):
    response = client.delete('/tags/1')
    assert response.status_code == 200