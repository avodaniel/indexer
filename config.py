import logging
import os
import socket

logger = logging.getLogger('indexer.config')

def cab_limit(self):
    return 20


def ensure_abs_path(f):
    def func():
        return os.path.abspath(f())
    return func


@ensure_abs_path
def db_path():
    return './data/db'


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port


def has_ipv6():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    try:
        s.connect(('ipv6.google.com', 0))
        return True
    except:
        return False


def server():
    if has_ipv6():
        return Server('::', 1024)
    else:
        return Server('0.0.0.0', 1024)
