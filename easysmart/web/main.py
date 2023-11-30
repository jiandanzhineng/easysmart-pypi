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


def build_response(msg=None, data=None, code=200, success=True, ):
    res = {
        'code': code,
        'success': success,
    }
    if data is not None:
        res['data'] = data
    if msg is not None:
        res['msg'] = msg
    return web.json_response(res)


class WebServer:

    def __init__(self, manager: 'Manager'):
        self.manager = manager

    async def web_start(self):
        app = web.Application()
        app.add_routes([web.get('/', self.handle),
                        web.get('/devices/', self.devices_view),
                        web.get('/device/{mac}/', self.device_get_view),
                        web.post('/device/{mac}/', self.device_set_view),
                        web.post('/device/{filter}/{detail}/', self.device_group_set_view),])
        await run_app(app, loop=asyncio.get_event_loop())

    async def handler(self, request):
        return build_response(data={'hello': 'world'})

    async def handle(self, request):
        name = request.match_info.get('name', "Anonymous")
        return build_response(msg=f'hello {name}')

    async def devices_view(self, request):
        devices = self.manager.devices
        d = []
        for mac, device in devices.items():
            d.append(device.to_dict())
        return build_response(data=d)

    async def device_get_view(self, request):
        mac = request.match_info.get('mac', "Anonymous")
        if mac in self.manager.devices:
            device = self.manager.devices[mac]
        else:
            return web.Response(text=json.dumps({'error': 'device not found'}))
        return build_response(data=device.to_dict())

    async def device_set_view(self, request):
        mac = request.match_info.get('mac', "Anonymous")
        if mac in self.manager.devices:
            device = self.manager.devices[mac]
        else:
            return build_response(success=False, msg='device not found')
        data = await request.post()
        for k, v in data.items():
            asyncio.gather(device.set_property(k, v))
        return build_response()

    async def device_group_set_view(self, request):
        filter = request.match_info.get('filter', "")
        detail = request.match_info.get('detail', "")
        if filter == "":
            return build_response(success=False, msg='filter is empty')
        if filter == 'all':
            devices = self.manager.devices
        else:
            devices = []
            for mac, device in self.manager.devices.items():
                device_detail = getattr(device, filter)
                if device_detail == detail:
                    devices.append(device)
        data = await request.post()
        for device in devices:
            for k, v in data.items():
                asyncio.gather(device.set_property(k, v))

        res = {
            'affected_devices': [device.mac for device in devices],
        }
        return build_response(data=res)
