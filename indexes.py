import config
from leveldb import LevelDB
import logging
import os
import os.path


logger = logging.getLogger('indexer.indexes')


class Indexes:
    class Error(Exception):
        def __init__(self, msg):
           super().__init__(msg) 

    def __init__(self):
        path = config.db_path()
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
            self._db = LevelDB(path)
        except Exception as e:
            raise Indexes.Error(f'Cannot open databse: {path}') from e

    # xpub index
    def xpub_to_addrs(self, xpub):
        """
        Key: XPUB, Returns: List of addresses.
        """
#       key = f'x{xpub}'
        raise NotImplementedError

    def addr_to_xpub(self, addr):
        """
        Key: Address, Returns: XPUB.
        """
#       key = f'a{addr}'
        raise NotImplementedError

    # address index
    def addr_to_txids(self, addr):
        """
        Key: Address. Returns: List of txids.
        """
#       key = f'A{addr}'
        raise NotImplementedError

    # txindex
    def txid_to_trans(self, txid):
        """
        Key: txid. Returns: Serialised transaction.
        """
#       key = f'T{txid}'
        raise NotImplementedError


indexes = Indexes()
