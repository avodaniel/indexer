#!/usr/bin/env python3

"""
    Listens for updates from BC. Uses ZMQ and python3's asyncio.

    Bitcoin should be started with the command line arguments:
        bitcoind -testnet -daemon \
                -zmqpubhashblock=tcp://ip.add.re.ss:port \
                -zmqpubrawtx=tcp://ip.add.re.ss:port \
                -zmqpubhashtx=tcp://ip.add.re.ss:port \
                -zmqpubhashblock=tcp://ip.add.re.ss:port

"""

import binascii
import asyncio
import zmq
import zmq.asyncio
import signal
import struct
import sys
import logging

import io
from bitcoin.messages import msg_tx

logger = logging.getLogger('indexer.zmq');

proto = 'tcp'
address = '172.16.11.17'
port = 1024

class ZMQHandler():
    def __init__(self):
        global proto
        global address
        global port

        self.loop = zmq.asyncio.install()
        self.zmqContext = zmq.asyncio.Context()

        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashtx")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawblock")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
        self.zmqSubSocket.connect(f"{proto}://{address}:{port}")

    async def handle(self) :
        msg = await self.zmqSubSocket.recv_multipart()
        topic = msg[0]
        body = msg[1]
        sequence = "Unknown"
        if len(msg[-1]) == 4:
          msgSequence = struct.unpack('<I', msg[-1])[-1]
          sequence = str(msgSequence)
        if topic == b"hashblock":
            logger.debug('HASH BLOCK (%s) -> %s', sequence, binascii.hexlify(body))
        elif topic == b"hashtx":
            logger.debug('HASH TX (%s) -> %s', sequence, binascii.hexlify(body))
        elif topic == b"rawblock":
            logger.debug('RAW BLOCK HEADER (%s) -> %s', sequence, binascii.hexlify(body[:80]))
        elif topic == b"rawtx":
            logger.debug('RAW TX (%s) -> %s', sequence, binascii.hexlify(body))
            tx = msg_tx.msg_deser(io.BytesIO(body))
            logger.debug('Parsed tx: %r', tx)
        # schedule ourselves to receive the next message
        asyncio.ensure_future(self.handle())

    def start(self):
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.create_task(self.handle())
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.zmqContext.destroy()

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('Starting ZMQ listener...')

daemon = ZMQHandler()
daemon.start()
