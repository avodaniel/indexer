import config

import asyncio
import sys
import logging

from daemon import Daemon
from indexes import indexes
from zmq_bc import ZMQHandler


# main
logger = logging.getLogger('indexer');
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('Starting ZMQ listener...')
logger.info('DB Path is: %s', config.db_path())

with Daemon() as daemon, ZMQHandler(sys.argv[1], sys.argv[2]) as zmq_handler:
    async def handle():
        transaction = await zmq_handler()
        logger.info('transaction: %s', transaction)
    daemon.start(handle)
