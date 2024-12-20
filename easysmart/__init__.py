import asyncio
import os
import pathlib
import sys
import threading
import time

from easysmart.manager import Manager
import zeroconf
import paho

from easysmart.mdns.mdns import mdns_register
from easysmart.mdns.mdns_async import mdns_async_register
from easysmart.mqtt_server.mqtt_server import start_emqx_server
from easysmart.web.webmain import WebServer


async def test_publish(manager):
    while True:
        await asyncio.sleep(5)
        print('publish')
        await manager.publish('/test/', 'hello world', 0)


def start_server(root_path=None, block=True, services=None):
    if sys.platform.lower() == "win32" or os.name.lower() == "nt":
        from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    if root_path is None:
        # get the root path of this project
        root_path = pathlib.Path(__file__).parent.parent.absolute()
        root_path = pathlib.Path(os.path.expanduser('~') + '/easysmart/')
    # 如果不存在则创建
    if not root_path.exists():
        root_path.mkdir()
    print(f'root path is {root_path}')
    # # start the manager
    # asyncio.gather(start_emqx_server(root_path))

    # create thread to register mdns
    thread = threading.Thread(target=mdns_register)
    thread.daemon = True
    thread.start()



    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # loop.run_until_complete(mdns_async_register())
    # manager = Manager()
    # asyncio.gather(manager.async_loop_start())
    # web_manager = WebServer(manager)
    # asyncio.gather(web_manager.web_start())
    # # asyncio.gather(test_publish(manager))

    main_manager = Manager()

    loop.create_task(async_start_server(root_path, main_manager, services=services), )
    print('main manager start')
    if block:
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print("stop server")
    else:
        return main_manager, loop
    # asyncio.run(main())


async def async_start_server(root_path=None, main_manager=None, services: list = None):
    print(f'async_start_server')
    print(f'root path is {root_path}')
    # asyncio.create_task(mdns_async_register())
    asyncio.create_task(start_emqx_server(root_path))
    asyncio.create_task(main_manager.async_loop_start())
    if services is None:
        services = []
    for service in services:
        s = service(main_manager)
        asyncio.create_task(s.start())
    while True:
        await asyncio.sleep(1)
