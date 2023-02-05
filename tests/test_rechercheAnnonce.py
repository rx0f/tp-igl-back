def test_index(app, client):
    res = client.post('/user/1/recherche_annonce' ,data = {
        'search': 'test'
        })
    assert res.json['data'] != None