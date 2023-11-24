import asyncio
import json
import logging
from asyncio import events
from typing import Optional

from aiohttp import web
from aiohttp.log import access_logger
from aiohttp.web import _run_app
from aiohttp.web_log import AccessLogger

from easysmart import Manager


async def run_app(
        app,
        *,
        host=None,
        port=None,
        path=None,
        sock=None,
        shutdown_timeout: float = 60.0,
        keepalive_timeout: float = 75.0,
        ssl_context=None,
        print=print,
        backlog: int = 128,
        access_log_class=AccessLogger,
        access_log_format: str = AccessLogger.LOG_FORMAT,
        access_log=access_logger,
        handle_signals: bool = True,
        reuse_address: Optional[bool] = None,
        reuse_port: Optional[bool] = None,
        handler_cancellation: bool = False,
        loop: Optional[asyncio.AbstractEventLoop] = None,
):
    """Run an app locally"""
    if loop is None:
        loop = asyncio.new_event_loop()

    # Configure if and only if in debugging mode and using the default logger
    if loop.get_debug() and access_log and access_log.name == "aiohttp.access":
        if access_log.level == logging.NOTSET:
            access_log.setLevel(logging.DEBUG)
        if not access_log.hasHandlers():
            access_log.addHandler(logging.StreamHandler())

    main_task = loop.create_task(
        _run_app(
            app,
            host=host,
            port=port,
            path=path,
            sock=sock,
            shutdown_timeout=shutdown_timeout,
            keepalive_timeout=keepalive_timeout,
            ssl_context=ssl_context,
            print=print,
            backlog=backlog,
            access_log_class=access_log_class,
            access_log_format=access_log_format,
            access_log=access_log,
            handle_signals=handle_signals,
            reuse_address=reuse_address,
            reuse_port=reuse_port,
            handler_cancellation=handler_cancellation,
        )
    )

    await main_task


class WebServer:

    def __init__(self, manager: 'Manager'):
        self.manager = manager

    async def web_start(self):
        app = web.Application()
        app.add_routes([web.get('/', self.handle),
                        web.get('/devices', self.devices_view)])
        await run_app(app, loop=asyncio.get_event_loop())
        return
        server = web.Server(self.handler)
        runner = web.ServerRunner(server)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()

        print("======= Serving on http://127.0.0.1:8080/ ======")

        while True:
            await asyncio.sleep(100 * 3600)

    async def handler(self, request):
        return web.Response(text='1')

    async def handle(self, request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)

    async def devices_view(self, request):
        devices = self.manager.devices
        d = []
        for mac, device in devices.items():
            d.append(device.to_dict())
        text = json.dumps(d)
        return web.Response(text=text)
