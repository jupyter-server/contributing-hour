import json

from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyter_server.base.handlers import APIHandler
import tornado


class RouteHandler(ExtensionHandlerMixin, APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server

    # @tornado.web.authenticated
    def get(self):
        name = self.get_argument("name", default="")
        age = self.get_argument("age", default="")
        if name and age:
            cursor = self.settings["cursor"]
            cursor.execute(f"INSERT INTO people VALUES ('{name}', '{age}') ")

        cursor.execute("SELECT * FROM people")
        rows = cursor.fetchall()
        data = [{"name": r["name"], "age": r["age"]} for r in rows]
        self.finish(json.dumps(data))
