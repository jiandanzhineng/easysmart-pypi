import asyncio
import pathlib
import time

from easysmart.manager import Manager
import zeroconf
import paho

from easysmart.mdns.mdns_async import mdns_async_register
from easysmart.mqtt_server.mqtt_server import start_emqx_server
from easysmart.web.main import WebServer


def start_server(root_path=None):
    if root_path is None:
        # get the root path of this project
        root_path = pathlib.Path(__file__).parent.parent.absolute()
    print(f'root path is {root_path}')
    # start the manager
    asyncio.gather(start_emqx_server(root_path))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mdns_async_register())
    manager = Manager()
    asyncio.gather(manager.async_loop_start())
    web_manager = WebServer(manager)
    asyncio.gather(web_manager.web_start())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("stop server")
    # asyncio.run(main())