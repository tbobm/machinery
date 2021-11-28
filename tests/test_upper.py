def test_upper_health(upper_client):
    """
    Check `/healthcheck` status code
    """
    rv = upper_client.get('/healthcheck')
    assert rv.status_code == 204

def test_upper_infos(upper_client):
    """
    Check `/infos` status code & type
    """
    rv = upper_client.get('/infos')
    assert rv.status_code == 200
    assert "name" in rv.get_json()

def test_upper_event(upper_client, valid_service_payload):
    """
    Check `/event` status code & type
    """
    rv = upper_client.post('/event', json=valid_service_payload)
    assert rv.status_code == 200
    assert "message" in rv.get_json()

def test_upper_event_failure_empty_json(upper_client):
    """
    Check `event` status code while sending empty json
    """
    rv = upper_client.post('/event', json={})
    assert rv.status_code == 400

def test_upper_event_failure_bad_json(upper_client, bad_generic_payload):
    """
    Check `event` status code while sending bad json
    """
    rv = upper_client.post('/event', json=bad_generic_payload)
    assert rv.status_code == 400