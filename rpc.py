import asyncio
import websockets

import config
import logging

import gen.py.rpc_pb2 as rpc_messages

logger = logging.getLogger('indexer.rpc')


async def _handler(wssp, req_uri):
    import datetime
    import random
    logger.debug('Request uri: %s', req_uri)
    while True:
        request = rpc_messages.Request()
        bytes = await wssp.recv()
        request.ParseFromString(bytes)
        logger.debug('Received: %s', request)
        rtype = request.WhichOneof('type')
        if rtype is None:
            pass
        elif (rtype == 'get_chain_info'):
            pass
        elif (rtype == 'get_tx'):
            pass
        elif (rtype == 'subscribe_addr'):
            pass
        else:
            pass

async def init_server():
    server = await websockets.server.serve(_handler, config.server().host, config.server().port)
