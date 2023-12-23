# 本脚本将控制一个跳蛋 每隔一秒进行一次开关
import asyncio

import easysmart as ezs


async def control_tiaodan(manager: ezs.Manager):
    onoff = True
    while True:
        for device in manager.devices.values():
            if device.device_type == 'TD01':  # 检测设备是否是跳蛋
                if onoff:
                    await device.set_property('power1', 255)
                    await device.set_property('power2', 255)
                else:
                    await device.set_property('power1', 0)
                    await device.set_property('power2', 0)
        onoff = not onoff
        await asyncio.sleep(1)


def main():
    # 启动服务器
    manager, loop = ezs.start_server(block=False)
    loop.create_task(control_tiaodan(manager))
    loop.run_forever()


if __name__ == '__main__':
    main()
