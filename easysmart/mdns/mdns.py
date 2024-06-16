#!/usr/bin/env python3

""" Example of announcing a service (in this case, a fake HTTP server) """

import argparse
import logging
import socket
import time
from time import sleep

from zeroconf import IPVersion, ServiceInfo, Zeroconf


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))  # 114.114.114.114也是dns地址
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def mdns_register():
    ip_version = IPVersion.V4Only
    desc = {'path': '/~paulsm/'}

    info = ServiceInfo(
        "_http._tcp.local.",
        "EasySmartSever._http._tcp.local.",
        addresses=[socket.inet_aton(get_host_ip())],
        port=80,
        properties=desc,
        server="easysmart.local.",
        host_ttl=60 * 60 * 60 * 60,  # 60*60 hours
        other_ttl=60 * 60 * 60 * 60,  # 60*60 hours
    )

    zeroconf = Zeroconf(ip_version=ip_version)
    print("Registration of a service")
    zeroconf.register_service(info)
    # try:
    #     while True:
    #         sleep(0.1)
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     print("Unregistering...")
    #     zeroconf.unregister_service(info)
    #     zeroconf.close()
    while True:
        time.sleep(1)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    mdns_register()
