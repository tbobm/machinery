def test_upper_health(client):
    """
    Check `/healthcheck` status code
    """
    rv = client.get('/healthcheck')
    assert rv.status_code == 204

def test_upper_infos(client):
    """
    Check `/infos` status code & type
    """
    rv = client.get('/infos')
    assert rv.status_code == 200
    assert "name" in rv.get_json()

def test_upper_event(client, valid_upper):
    """
    Check `/event` status code & type
    """
    rv = client.post('/event', json=valid_upper)
    assert rv.status_code == 200
    assert "message" in rv.get_json()

def test_upper_event_failure_not_json(client):
    """
    Check `event` status code while not sending json
    """
    rv = client.post('/event', 'notjson')
    assert rv.status_code == 415

def test_upper_event_failure_empty_json(client):
    """
    Check `event` status code while sending empty json
    """
    rv = client.post('/event', json={})
    assert rv.status_code == 400

def test_upper_event_failure_bad_json(client, bad_generic_payload):
    """
    Check `event` status code while sending bad json
    """
    rv = client.post('/event', json=bad_generic_payload)
    assert rv.status_code == 400