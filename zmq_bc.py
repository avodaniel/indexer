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
import traceback
from bitcoinrpc.asyncio.authproxy import AuthServiceProxy, JSONRPCException

logger = logging.getLogger('indexer.zmq');

class ZMQHandler():
    class Tx:
        def __init__(self):
            self.hash = None
            self.body = None


        def is_everything_set(self):
            return self.hash is not None and self.body is not None

        def __str__(self):
            return f'Tx:{self.hash}: {self.body}'


    def __init__(self, zmq_endpoint, rpc_addr):
        self.zmq_endpoint = zmq_endpoint
        self.rpc_addr = rpc_addr
        self.rpc = AuthServiceProxy(self.rpc_addr)

        self._txs = dict()

        self.zmqContext = zmq.asyncio.Context()

        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashtx")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawblock")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
        self.zmqSubSocket.connect(self.zmq_endpoint)

    async def _process_tr(self, tx_id):
        tx = self._txs[tx_id]
        if not tx.is_everything_set():
            return

        transaction = None
        if transaction is None:
            try:
                transaction = await self.rpc.getrawtransaction(tx.hash, 1)
            except JSONRPCException:
                traceback.print_exc()
                pass
        if transaction is None:
            try:
                transaction = await self.rpc.gettransaction(tx.hash)
            except JSONRPCException:
                traceback.print_exc()
                pass
        if transaction is None:
            logger.error('Cannot decode transaction: %s', tx)
        else:
            logger.debug('Tx received: %s, transaction: %s', tx, transaction)
        del self._txs[tx_id]
        return transaction

    async def __call__(self):
        while True:
            msg = await self.zmqSubSocket.recv_multipart()
            topic = msg[0]
            body = msg[1]
            sequence = "Unknown"
            transaction = None
            if len(msg[-1]) == 4:
              msgSequence = struct.unpack('<I', msg[-1])[-1]
              sequence = str(msgSequence)
            if topic == b"hashblock":
                logger.debug('HASH BLOCK (%s) -> %s', sequence, binascii.hexlify(body))
            elif topic == b"hashtx":
                logger.debug('HASH TX (%s) -> %s', sequence, binascii.hexlify(body))
                self._txs.setdefault(sequence, ZMQHandler.Tx()).hash = binascii.hexlify(body).decode('ascii')
                transaction = await self._process_tr(sequence)
            elif topic == b"rawblock":
                logger.debug('RAW BLOCK HEADER (%s) -> %s', sequence, binascii.hexlify(body[:80]))
            elif topic == b"rawtx":
                logger.debug('RAW TX (%s) -> %s', sequence, binascii.hexlify(body))
                self._txs.setdefault(sequence, ZMQHandler.Tx()).body = body
                transaction = await self._process_tr(sequence)
            if transaction is not None:
                return transaction

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zmqContext.destroy()
