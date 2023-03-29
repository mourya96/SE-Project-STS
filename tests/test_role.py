import json


def test_role(client):
    # Make a GET request to Role API
    response = client.get('/api/role')
    # Check status of response
    assert response.status_code == 200
