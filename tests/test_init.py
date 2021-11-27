import machinery.api

def test_app():
    assert machinery.api.create_app() is not None
