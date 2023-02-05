def test_index(app, client):
    res = client.get('/user/1')
    assert res.status_code == 200
    assert res != None