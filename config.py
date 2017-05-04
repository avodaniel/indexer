import logging
import os

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
