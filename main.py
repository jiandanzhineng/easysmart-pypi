import os
import sys
import time
import asyncio

from easysmart import start_server
from easysmart.mdns.mdns_async import mdns_async_register





if __name__ == '__main__':
    print('start server')
    start_server()



