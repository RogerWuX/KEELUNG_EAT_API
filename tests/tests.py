import sys
sys.path.append("..")
import pytest


@pytest.fixture(scope='module')
def client():
	import KeelungEat
	return KeelungEat.app.test_client()
	
def test_post(client):
    rv = client.get('/')
    assert rv.status_code == 200
