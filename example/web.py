# 本脚本将开启一个web服务，提供接口
# 接口文档 https://console-docs.apipost.cn/preview/91b7075b8e535790/83ff4d1e5753d015

import easysmart as ezs
from easysmart.web.webmain import WebServer


def main():
    # 启动服务器
    services = [WebServer]
    manager, loop = ezs.start_server(block=False, services=services)
    loop.run_forever()


if __name__ == '__main__':
    main()
