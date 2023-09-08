import pytest

from ..yorkorthodox_rest import app


@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True,
    })
    return app.test_client()
