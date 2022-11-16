import sys
import os
home = os.environ['HOME']
sys.path.append(home + '/cop4521')
print(sys.path)
from app import app as myapp


import pytest

@pytest.fixture()
def app():
    myapp.config.update({
        "TESTING": True,
    })

    yield myapp

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_basic_routes(client):
    routes = [
            "/",
            "/home",
            "/about",
            ]
    for route in routes:
        res = client.get(route)
        print(res)
        assert res.status_code == 200

