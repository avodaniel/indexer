import config
from leveldb import LevelDB
import logging
import os


logger = logging.getLogger('indexer.indexes')


class Indexes:
    class Error(Exception):
        def __init__(self, msg):
           super().__init__(msg) 

    def __init__(self):
        path = config.db_path()
        try:
            os.makedirs(path)
            self._db = LevelDB(path)
        except Exception as e:
            raise Indexes.Error(f'Cannot open databse: {path}') from e


indexes = Indexes()
