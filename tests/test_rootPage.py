import json

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = 'Hello, World!'
    assert expected == res.get_data(as_text=True)