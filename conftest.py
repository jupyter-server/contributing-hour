import pytest

pytest_plugins = ["jupyter_server.pytest_plugin"]


@pytest.fixture
def jp_server_config():
    return {
        "ServerApp": {
            "jpserver_extensions": {
                "contrib_hour": True
        }}}