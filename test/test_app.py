import json
from app import *

def test_home(app, client):
    response = client.get("/")
    assert response.status_code == 200

def test_predict(app, client):
    response = app.test_client().post("/results",data=json.dumps({"inputs":[["FB",5]]}),
    content_type="application/json") 
    assert response.status_code == 200
    assert response.data == b'{"Predicted House Price in Dollars": 28.99}'