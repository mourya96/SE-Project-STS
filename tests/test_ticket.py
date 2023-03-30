import json
from pprint import pprint


def test_get_tickets(client):
    params = {
        "limit": 3,
        "TagName": "week 1",
        "search": "titl"
    }
    url = "http://127.0.0.1:5500/api/subject/subject_1"
    res = client.get(url, query_string=params)
    json_data = json.loads(res.data)
    pprint(json_data)
    assert res.status_code == 200
    assert len(json_data) <= params["limit"]
    for obj in json_data:
        assert obj['subject_name'] == "subject_1"
        assert obj["sec_name"] == params['TagName']
        assert params['search'].lower() in obj['title'].lower()


def test_get_tickets_error(client):
    url = "http://127.0.0.1:5500/api/subject/NotASubject"
    res = client.get(url)
    assert res.status_code == 404
    json_data = json.loads(res.data)
    assert json_data['error_code'] == 'TICKET006'
