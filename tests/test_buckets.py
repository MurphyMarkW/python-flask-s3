import pytest


@pytest.fixture
def app():
    """ Application test client.
    """
    import flask
    import flasks3

    app = flask.Flask(__name__)

    app.config['flasks3'] = {
        'authenticate': flasks3.auth.basic('some','user'),
        'driver': flasks3.drivers.local.LocalStorageDriver('.'),
    }

    app.register_blueprint(flasks3.blueprint)

    return app.test_client()

def test_get_service(app):
    """Tests that GET / returns a bucket list.
    """
    buckets = app.get('/')
    #buckets = conn.get_all_buckets()

    assert buckets

def test_get_bucket(app):
    """Tests that GET /<bucket>/ returns a bucket manifest.
    """
    #bucket = conn.get_bucket('bucket')
    bucket = app.get('/bucket/')

    assert bucket

def test_get_key(app):
    """Tests that GET /<bucket>/<key> returns key data.
    """
    #key = conn.get_bucket('bucket').get_key('key/other/key').get_contents_as_string()
    key = app.get('/bucket/key')

    assert key
