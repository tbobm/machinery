def test_reverse_health(reverse_client):
    """
    Check `/healthcheck` status code
    """
    rv = reverse_client.get('/healthcheck')
    assert rv.status_code == 204

def test_reverse_infos(reverse_client):
    """
    Check `/infos` status code & type
    """
    rv = reverse_client.get('/infos')
    assert rv.status_code == 200
    assert "name" in rv.get_json()

def test_reverse_event(reverse_client, valid_service_payload):
    """
    Check `/event` status code & type
    """
    rv = reverse_client.post('/event', json=valid_service_payload)
    assert rv.status_code == 200
    assert "message" in rv.get_json()

def test_reverse_event_failure_empty_json(reverse_client):
    """
    Check `event` status code while sending empty json
    """
    rv = reverse_client.post('/event', json={})
    assert rv.status_code == 400

def test_reverse_event_failure_bad_json(reverse_client, bad_generic_payload):
    """
    Check `event` status code while sending bad json
    """
    rv = reverse_client.post('/event', json=bad_generic_payload)
    assert rv.status_code == 400