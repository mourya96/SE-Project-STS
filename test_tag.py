import json


def test_subject_tag(client):
    response = client.get(f'/api/tag/subject/1')
    assert response.status_code == 200


def test_secondary_tag(client):
    response = client.get(f'/api/tag/secondary/1')
    assert response.status_code == 200


def test_create_subject_tag(client):
    # Set up test data
    new_tag = {'tag_name': 'MAD-1'}
    # Make POST request to create new tag
    response = client.post('/api/tag/subject', json=new_tag)

    # Check status code of response
    assert response.status_code == 201

    # Check response body for correct tag-name
    data = json.loads(response.data)
    assert data['subject_name'] == 'MAD-1'
    client.delete(f'/api/tag/subject/{data["subject_id"]}')


def test_create_secondary_tag(client):
    # Set up test data
    new_tag = {'tag_name': 'Quiz-1'}
    # Make POST request to create new tag
    response = client.post('/api/tag/secondary', json=new_tag)

    # Check status code of response
    assert response.status_code == 201

    # Check response body for correct tag-name
    data = json.loads(response.data)
    assert data['sec_name'] == 'Quiz-1'
    client.delete(f'/api/tag/secondary/{data["sec_id"]}')


def test_edit_secondary_tag(client):
    # Set up test data
    new_tag = {'tag_name': 'Quiz-1'}
    # Make POST request to create new tag
    response = client.post('/api/tag/secondary', json=new_tag)

    # Check status code of response
    assert response.status_code == 201

    data = json.loads(response.data)
    # Set up edit data
    edit_data = {'tag_name': 'quiz-1'}
    # Make PUT request to edit that tag
    response = client.put(f'/api/tag/secondary/{data["sec_id"]}',
                          json=edit_data)

    # Check status code of response
    assert response.status_code == 202

    data = json.loads(response.data)
    assert data['sec_name'] == 'quiz-1'
    client.delete(f'/api/tag/secondary/{data["sec_id"]}')
