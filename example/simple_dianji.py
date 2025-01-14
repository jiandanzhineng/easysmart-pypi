# 本脚本将控制电击器 每秒有50%的几率开启电击器，电击器开启时间为1秒，电压为30V
import asyncio

import easysmart as ezs
import time
import random

async def control_dianji(manager: ezs.Manager):
    onoff = True
    s = time.time()
    run_flag = True
    while True:
        for device in manager.devices.values():
            if device.device_type == 'DIANJI' and random.random() < 0.5:  # 检测设备是否是跳蛋
                new_data = {
                    'method': 'dian',
                    'voltage': 30,
                    'time': 1000
                }
                await device.publish(new_data)

        onoff = not onoff
        await asyncio.sleep(1)


def main():
    # 启动服务器
    manager, loop = ezs.start_server(block=False)
    loop.create_task(control_dianji(manager))
    loop.run_forever()


if __name__ == '__main__':
    main()
