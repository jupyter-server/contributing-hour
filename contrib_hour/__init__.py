from .handlers import MyExtensionHandler, MyWebsocketHandler
from jupyter_server.utils import url_path_join


def _load_jupyter_server_extension(serverapp):
    """
    This function is called when the extension is loaded.
    """
    handlers = [
        (url_path_join(serverapp.base_url, 'hello'), MyExtensionHandler),
        (url_path_join(serverapp.base_url, 'websocket'), MyWebsocketHandler, {"db": []})
    ]
    serverapp.web_app.add_handlers('.*$', handlers)
