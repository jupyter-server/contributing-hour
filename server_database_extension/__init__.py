"""A Jupyter Server extension."""
from .extension import Extension
__version__ = "0.1.0"


def _jupyter_server_extension_points():
    return [{
        "module": "server_database_extension",
        "app": Extension
    }]
