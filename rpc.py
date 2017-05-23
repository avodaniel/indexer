import asyncio
import websockets

import config
import logging
import traceback

import gen.py.rpc_pb2 as rpc_messages

logger = logging.getLogger('indexer.rpc')


class RpcError(Exception):
    def whoami(self):
        return self.__class__.__name__

class RpcNotImplementedError(RpcError):
    pass

class RpcUnknownRequest(RpcError):
    pass

class RpcEmptyRequest(RpcError):
    pass

async def _handler(wssp, req_uri):
    import datetime
    import random
    logger.debug('R:%s L:%s Established connection: path:%s', wssp.remote_address, wssp.local_address, req_uri)
    try:
        while True:
            request = rpc_messages.Request()
            response = rpc_messages.Response()
            bytes = await wssp.recv()
            request.ParseFromString(bytes)
            logger.debug("R:%s L:%s Received request:%s", wssp.remote_address, wssp.local_address, request)
            rtype = request.WhichOneof('request')
            try:
                if rtype is None:
                    raise RpcEmptyRequest
                elif (rtype == 'get_chain_info'):
                    raise RpcNotImplementedError
                elif (rtype == 'get_tx'):
                    raise RpcNotImplementedError
                elif (rtype == 'subscribe_addr'):
                    raise RpcNotImplementedError
                else:
                    raise RpcUnknownRequest
            except RpcError as e:
                response.error.msg = e.whoami()
            logger.debug("R:%s L:%s Sending msg:%r", wssp.remote_address, wssp.local_address, response.SerializeToString())
            await wssp.send(response.SerializeToString())
    except websockets.exceptions.ConnectionClosed:
        logger.info("R:%s L:%s The remote side has closed the connection", wssp.remote_address, wssp.local_address)

async def init_server():
    server = await websockets.server.serve(_handler, config.server().host, config.server().port)
