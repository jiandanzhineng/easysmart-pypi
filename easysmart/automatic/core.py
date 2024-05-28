import asyncio

from easysmart import Manager


class AutomaticCore(object):
    def __init__(self):
        pass

    def run(self):
        pass

    async def start(self):
        ...

    async def on_message_cb(self, topic, payload):
        pass

    async def on_device_connect(self):
        pass

    async def on_device_value_change(self):
        pass

    async def on_device_action(self):
        pass

    async def on_device_disconnect_cb(self):
        pass

    async def on_message(self, topic, payload):
        pass


'''
1. 触发条件
时间，设备动作，设备属性变化，设备连接，设备断开
2. 执行动作
'''
