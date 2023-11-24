import os
import sys
import time
import asyncio

from easysmart import start_server
from easysmart.mdns.mdns_async import mdns_async_register





if __name__ == '__main__':
    print('start server')
    if sys.platform.lower() == "win32" or os.name.lower() == "nt":
        from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    start_server()


