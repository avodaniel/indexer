import asyncio
import signal
import logging
import zmq
import zmq.asyncio

logger = logging.getLogger('indexer.daemon');

class Daemon:
    def __init__(self):
        self.loop = zmq.asyncio.install()

    def start(self, init, handler):
        async def handle():
            await handler()
            asyncio.ensure_future(handle())
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.run_until_complete(init())
        self.loop.create_task(handle())
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False
