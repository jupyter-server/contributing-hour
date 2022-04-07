import asyncio

from jupyter_server.base.handlers import JupyterHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback


class MyExtensionHandler(JupyterHandler):

    def get(self):
        self.write("""
<script>
    // Create WebSocket connection.
    const socket = new WebSocket('ws://localhost:8888/websocket');

    // Connection opened
    socket.addEventListener('open', function (event) {
        socket.send('Hello Server!');
    });

    // Listen for messages
    socket.addEventListener('message', function (event) {
        console.log('Message from server ', event.data);

        document.write(`<h1>${event.data}</h1>`);

    });
</script>

        """)
        print("hello, world!")


class MyWebsocketHandler(JupyterHandler, WebSocketHandler):

    @property
    def last_message(self):
        return self.db[-1]

    def initialize(self, *args, **kwargs):
        self.db = kwargs.pop("db", None)
        super().initialize(*args, **kwargs)

    async def open(self):

        async def spam():
            while True:
                await asyncio.sleep(5)
                await self.write_message(f"Length of db: {len(self.db)}")

        loop = asyncio.get_running_loop()
        loop.call_soon(spam)
        return super().open()

    async def on_message(self, message):
        print(f"it wrote a message: {message}")
        self.db.append(message)
        await self.write_message(message)

    def on_close(self):
        pass
