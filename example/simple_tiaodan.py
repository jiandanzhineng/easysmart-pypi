# 本脚本将控制一个跳蛋 每隔一秒进行一次开关
import asyncio

import easysmart as ezs
import time


async def control_tiaodan(manager: ezs.Manager):
    onoff = True
    s = time.time()
    run_flag = True
    while True:
        for device in manager.devices.values():
            if device.device_type == 'TD01':  # 检测设备是否是跳蛋
                if onoff:
                    properties = {
                        'power1': 255,
                        'power2': 255,
                    }
                    await device.set_multi_properties(properties)
                else:
                    properties = {
                        'power1': 0,
                        'power2': 0,
                    }
                    await device.set_multi_properties(properties)
        # if len(manager.devices) == 0 and time.time() - s > 30:
        #     run_flag = False

        onoff = not onoff
        await asyncio.sleep(2)


def main():
    # 启动服务器
    manager, loop = ezs.start_server(block=False)
    loop.create_task(control_tiaodan(manager))
    loop.run_forever()


if __name__ == '__main__':
    main()
