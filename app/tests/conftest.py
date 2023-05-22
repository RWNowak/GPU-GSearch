import os, pytest
from .. import create_app

# TESTING CLIENT FOR FUNCTIONAL TESTS

@pytest.fixture(scope='module')
def test_client():  
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client 