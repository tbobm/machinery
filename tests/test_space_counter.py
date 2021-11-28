def test_space_counter_health(space_counter_client):
    """
    Check `/healthcheck` status code
    """
    rv = space_counter_client.get('/healthcheck')
    assert rv.status_code == 204

def test_space_counter_infos(space_counter_client):
    """
    Check `/infos` status code & type
    """
    rv = space_counter_client.get('/infos')
    assert rv.status_code == 200
    assert "name" in rv.get_json()

def test_space_counter_event(space_counter_client, valid_space_counter):
    """
    Check `/event` status code & type
    """
    rv = space_counter_client.post('/event', json=valid_space_counter)
    assert rv.status_code == 200
    assert "message" in rv.get_json()

def test_space_counter_event_failure_empty_json(space_counter_client):
    """
    Check `event` status code while sending empty json
    """
    rv = space_counter_client.post('/event', json={})
    assert rv.status_code == 400

def test_space_counter_event_failure_bad_json(space_counter_client, bad_generic_payload):
    """
    Check `event` status code while sending bad json
    """
    rv = space_counter_client.post('/event', json=bad_generic_payload)
    assert rv.status_code == 400