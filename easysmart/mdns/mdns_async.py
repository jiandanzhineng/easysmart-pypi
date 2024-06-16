#!/usr/bin/env python3
"""Example of announcing 250 services (in this case, a fake HTTP server)."""

import argparse
import asyncio
import logging
import socket
from typing import List, Optional

from zeroconf import IPVersion
from zeroconf.asyncio import AsyncServiceInfo, AsyncZeroconf


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))  # 114.114.114.114也是dns地址
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


async def mdns_async_register():
    ip_version = IPVersion.V4Only
    desc = {'path': '/~paulsm/'}

    info = AsyncServiceInfo(
        "_http._tcp.local.",
        "EasySmartSever._http._tcp.local.",
        addresses=[socket.inet_aton(get_host_ip())],
        port=80,
        properties=desc,
        server="easysmart.local.",
        host_ttl=60 * 60 * 60 * 60,  # 60*60 hours
        other_ttl=60 * 60 * 60 * 60,  # 60*60 hours
    )
    runner = AsyncMdnsRunner(IPVersion.V4Only)
    await runner.register_services([info])
    while True:
        await asyncio.sleep(10)


class AsyncMdnsRunner:
    tag = 'MDNSRunner'
    def __init__(self, ip_version: IPVersion) -> None:
        self.ip_version = ip_version
        self.aiozc: Optional[AsyncZeroconf] = None

    async def register_services(self, infos: List[AsyncServiceInfo]) -> None:
        self.aiozc = AsyncZeroconf(ip_version=self.ip_version)
        tasks = [self.aiozc.async_register_service(info) for info in infos]
        background_tasks = await asyncio.gather(*tasks)
        await asyncio.gather(*background_tasks)
        print(f'[{self.tag}] register_services success')
        # while True:
        #     await asyncio.sleep(1)

    async def async_update_service(self, info: AsyncServiceInfo) -> None:
        assert self.aiozc is not None
        await self.aiozc.async_update_service(info)

    async def unregister_services(self, infos: List[AsyncServiceInfo]) -> None:
        assert self.aiozc is not None
        tasks = [self.aiozc.async_unregister_service(info) for info in infos]
        background_tasks = await asyncio.gather(*tasks)
        await asyncio.gather(*background_tasks)
        await self.aiozc.async_close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument('--v6', action='store_true')
    version_group.add_argument('--v6-only', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)
    if args.v6:
        ip_version = IPVersion.All
    elif args.v6_only:
        ip_version = IPVersion.V6Only
    else:
        ip_version = IPVersion.V4Only

    infos = []
    for i in range(250):
        infos.append(
            AsyncServiceInfo(
                "_http._tcp.local.",
                f"Paul's Test Web Site {i}._http._tcp.local.",
                addresses=[socket.inet_aton("127.0.0.1")],
                port=80,
                properties={'path': '/~paulsm/'},
                server=f"zcdemohost-{i}.local.",
            )
        )

    print("Registration of 250 services...")
    loop = asyncio.get_event_loop()
    runner = AsyncMdnsRunner(ip_version)
    try:
        loop.run_until_complete(runner.register_services(infos))
    except KeyboardInterrupt:
        loop.run_until_complete(runner.unregister_services(infos))
