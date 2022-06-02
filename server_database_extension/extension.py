import sqlite3
import pathlib
from traitlets import Unicode, validate, TraitError
from jupyter_server.extension.application import ExtensionApp
from .handlers import RouteHandler


class DatabaseExtension(ExtensionApp):

    name = "server_database_extension"
    handlers = [
        ("/test", RouteHandler)
    ]

    database_filepath = Unicode(
        default_value=":memory:",
        help=(
            "The filesystem path to SQLite Database file "
            "(e.g. /path/to/session_database.db). By default, the session "
            "database is stored in-memory (i.e. `:memory:` setting from sqlite3) "
            "and does not persist when the current Jupyter Server shuts down."
        ),
    ).tag(config=True)

    @validate("database_filepath")
    def _validate_database_filepath(self, proposal):
        value = proposal["value"]
        if value == ":memory:":
            return value
        path = pathlib.Path(value)
        if path.exists():
            # Verify that the database path is not a directory.
            if path.is_dir():
                raise TraitError(
                    "`database_filepath` expected a file path, but the given path is a directory."
                )
            # Verify that database path is an SQLite 3 Database by checking its header.
            with open(value, "rb") as f:
                header = f.read(100)

            if not header.startswith(b"SQLite format 3") and not header == b"":
                raise TraitError(
                    "The given file is not an SQLite database file.")
        return value

    # Session database initialized below
    _cursor = None
    _connection = None
    _columns = {"name", "age"}

    @property
    def cursor(self):
        """Start a cursor and create a database called 'session'"""
        if self._cursor is None:
            self._cursor = self.connection.cursor()
            self._cursor.execute(
                """CREATE TABLE IF NOT EXISTS people
                (name, age)"""
            )
        return self._cursor

    @property
    def connection(self):
        """Start a database connection"""
        if self._connection is None:
            # Set isolation level to None to autocommit all changes to the database.
            self._connection = sqlite3.connect(
                self.database_filepath, isolation_level=None)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close(self):
        """Close the sqlite connection"""
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

    def __del__(self):
        """Close connection once SessionManager closes"""
        self.close()

    def initialize_configurables(self):
        self.cursor

    def initialize_settings(self):
        self.initialize_configurables()
        self.settings["cursor"] = self.cursor
