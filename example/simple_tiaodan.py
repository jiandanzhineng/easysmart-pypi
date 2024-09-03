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
            if device.device_type == 'TD01' and run_flag:  # 检测设备是否是跳蛋
                if onoff:
                    await device.set_property('power1', 255)
                    await device.set_property('power2', 255)
                else:
                    await device.set_property('power1', 0)
                    await device.set_property('power2', 0)
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
