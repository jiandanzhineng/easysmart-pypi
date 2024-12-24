# 压力测试
import asyncio

import easysmart as ezs
import time
import json
import random


async def pressure(manager: ezs.Manager, loop=None):
    onoff = True
    s = time.time()
    run_flag = True
    while True:
        topic = '/all'
        voltage = int(50 * random.random()) + 50
        payload = {
            "method": "update",
            "voltage":voltage,
            "delay":30,
            "shock":1
        }
        payload = json.dumps(payload)
        print(f'pressure publish: {topic} {payload}')
        loop.create_task(manager.publish(topic, payload))
        await asyncio.sleep(0.2)


def main():
    # 启动服务器
    manager, loop = ezs.start_server(block=False)
    loop.create_task(pressure(manager, loop=loop))
    loop.run_forever()


if __name__ == '__main__':
    main()
