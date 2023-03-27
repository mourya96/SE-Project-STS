import json


def test_subject_tag(client):
    response = client.get(f'/api/tag/subject/1')
    assert json.loads(response.data)['subject_name'] == 'BA'
