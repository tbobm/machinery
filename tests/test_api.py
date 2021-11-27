def test_api_health(client):
    """Start with a blank database."""

    rv = client.get('/healthcheck')
    assert rv.status_code == 204


def test_create_service(client, valid_service):
    rv = client.post('/s', json=valid_service)

    assert rv.status_code == 201
