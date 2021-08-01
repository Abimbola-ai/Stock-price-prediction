from app import *

def test_home(app, client):
    response = client.get("/")
    assert response.status_code == 200
