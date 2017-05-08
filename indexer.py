import config

import asyncio
import sys
import logging

from daemon import Daemon
from indexes import indexes
import rpc
from zmq_bc import ZMQHandler


# main

for m in ( ('indexer', logging.DEBUG), ('websockets', logging.ERROR)):
    logger = logging.getLogger(m[0])
    logger.setLevel(m[1])
    ch = logging.StreamHandler()
    ch.setLevel(m[1])
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

logger = logging.getLogger('indexer')
logger.info('Starting ZMQ listener...')
logger.info('DB Path is: %s', config.db_path())

with Daemon() as daemon, ZMQHandler(sys.argv[1], sys.argv[2]) as zmq_handler:
    async def init():
        await rpc.init_server()
    async def handle():
        transaction = await zmq_handler()
        logger.info('transaction: %s', transaction)
    daemon.start(init=init, handler=handle)
