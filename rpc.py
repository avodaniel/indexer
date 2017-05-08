import asyncio
import websockets

import config
import logging

logger = logging.getLogger('indexer.rpc')


async def _handler(wssp, req_uri):
    import datetime
    import random
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await wssp.send(now)
        await asyncio.sleep(random.random() * 3)


async def init_server():
    server = await websockets.server.serve(_handler, config.server().host, config.server().port)
