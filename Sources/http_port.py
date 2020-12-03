# -*- coding: utf-8 -*-

import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

__session__ : requests.Session


class SourcePortAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to set the source port."""

    def __init__(self, port, *args, **kwargs):
        self._source_port = port
        super(SourcePortAdapter, self).__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, source_address=('', self._source_port))


def init(port: int) -> requests.Session:
    global __session__
    __session__ = requests.Session()
    __session__.mount('http://', SourcePortAdapter(port))
    __session__.mount('https://', SourcePortAdapter(port))
    return __session__


def uninit():
    global __session__
    __session__.close()
    del __session__