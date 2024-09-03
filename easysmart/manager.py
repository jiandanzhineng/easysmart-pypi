import asyncio
import json
import os
import threading
import time
import traceback
import warnings

import aiomqtt

from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from paho.mqtt import client as mqtt
from easysmart.device.base_device import BaseDevice


def on_log(client, userdata, level, buf):
    if level == MQTT_LOG_INFO:
        head = 'INFO'
    elif level == MQTT_LOG_NOTICE:
        head = 'NOTICE'
    elif level == MQTT_LOG_WARNING:
        head = 'WARN'
    elif level == MQTT_LOG_ERR:
        head = 'ERR'
    elif level == MQTT_LOG_DEBUG:
        head = 'DEBUG'
    else:
        head = level
    print('%s: %s' % (head, buf))


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    # client.subscribe(topic, 0)


def on_message(client, userdata, msg):
    print('topic:' + msg.topic + ' ' + str(msg.payload))
    try:
        data = json.loads(msg.payload)
    except:
        data = str(msg.payload)
    print(f'{data}')


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected disconnection %s' % rc)


class Manager:
    client = None
    automation = None

    def __init__(self, on_message_cb=None, on_device_disconnect_cb=None):
        self.client_id = 'MQTT_MAIN' + os.urandom(6).hex()

        self.on_message_cb = on_message_cb
        self.on_device_disconnect_cb = on_device_disconnect_cb

        self.devices = {}

    def subscribe(self, *args, **kwargs):
        return self.client.subscribe(*args, **kwargs)

    async def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        print(f'publish: {topic} {payload}')
        await self.client.publish(topic=topic, payload=payload, qos=qos, retain=retain, properties=properties)
        # return self.client.publish(topic, payload, qos, retain, properties)

    def loop_forever(self):
        self.client.loop_start()
        self.thread_main()

    def loop_start(self):
        # self._thread_terminate = False
        # self._thread = threading.Thread(target=self.thread_main)
        # self._thread.daemon = True
        # self._thread.start()
        return self.client.loop_start()

    async def thread_main(self):
        """
        主线程
        :return: None
        """
        while True:
            await asyncio.sleep(1)
            await self._seconds_work()

    async def _seconds_work(self):
        """
        每秒被调用一次
        :return: None
        """
        # print('seconds work')
        # print 当前设备列表
        # print('devices:')
        need_del = []
        for k, v in self.devices.items():
            # print(f'{k}: {v}')
            if time.time() - v.last_active_time > 30:
                print(f'device {k} offline')
                need_del.append(k)
        for k in need_del:
            self.devices.pop(k)

    async def async_loop_start(self):
        print('启动主服务循环')
        fail_num = 0
        debug = True
        if debug: warnings.warn('debug mode is on')
        loop = asyncio.get_event_loop()
        loop.create_task(self.thread_main())
        while True:
            try:
                await self._async_loop_start()
            except aiomqtt.error.MqttError as e:
                print(f'[{fail_num}]async_loop_start connect error: {e}')
                fail_num += 1
                await asyncio.sleep(3)
            except Exception as e:
                print(f'[{fail_num}]async_loop_start error: {e}')
                if debug: traceback.print_exc()
                fail_num += 1
                await asyncio.sleep(3)

    async def _async_loop_start(self):
        async with aiomqtt.Client("easysmart.local") as self.client:
            while True:
                try:
                    print('sub #')
                    await self.client.subscribe("/#")
                    print('sub /dpub/#')
                    await self.client.subscribe("/dpub/#")
                    print('sub /all/')
                    await self.client.subscribe("/all/")
                    break
                except Exception as e:
                    print(f'async_loop_start error: {e}')
                    await asyncio.sleep(1)
            print('sub success')
            while True:
                try:
                    async with self.client.messages() as messages:
                        async for message in messages:
                            payload = message.payload.decode('utf-8')
                            topic = message.topic
                            # print hh:mm:ss topic payload
                            print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}]: '
                                  f'{topic}|{payload}')
                            try:
                                data = json.loads(payload)
                            except:
                                data = str(payload)
                                print(f'json.loads error: {data}')
                                continue
                            # await self.msg_process(message, data)
                            asyncio.create_task(self.msg_process(message, data))
                except Exception as e:
                    print(f'async_loop_start error: {e}')
                    await asyncio.sleep(1)

    def load_auto_config(self):
        if self.automation:
            ...

    def init_sync_mqtt_client(self):
        self.client = mqtt.Client(self.client_id, protocol=mqtt.MQTTv311, clean_session=False)
        self.client.on_log = on_log
        self.client.on_connect = on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = on_disconnect
        self.client.connect('easysmart.local', 1883, 60)
        self.client.loop_start()
        self.client.subscribe('#', 0)
        self.client.subscribe('/dpub/#', 1)
        self.client.subscribe('/all/', 1)
        self.client.subscribe('/test/', 1)
        self.client.publish('/test', 'hello world', 0)

    async def msg_process(self, msg, data):
        await self._msg_process(msg, data)
        if self.on_message_cb is not None:
            asyncio.gather(self.on_message_cb(msg, data))

    async def _msg_process(self, msg, data):
        topic = msg.topic.value
        # 如果topic形式为 /dpub/{mac}
        if topic.startswith('/dpub/'):
            mac = topic[6:]
            if mac not in self.devices:
                if data.get('method') == 'report':
                    self.devices[mac] = BaseDevice(mac, data.get('device_type', ''), mqtt_client=self.client)
                    print(f'new device {mac}')
                else:
                    print(f'unknown device {mac} 等待该设备的report信息')
                    return
            self.devices[mac].last_active_time = time.time() # 更新设备活跃时间
            method = data.get('method')
            if method == 'report':
                new_data = data.copy()
                new_data.pop('method')
                for k, v in new_data.items():
                    self.devices[mac].update(k, v)
            elif method == 'update':
                key = data.get('key')
                value = data.get('value')
                if key and value:
                    self.devices[mac].update(key, value)

    def get_device(self, mac=None, device_type=None):
        devices = []
        for k, v in self.devices.items():
            if mac and mac != k:
                continue
            if device_type and device_type != v.device_type:
                continue
            devices.append(v)
        return devices


if __name__ == '__main__':
    m = Manager()
    m.loop_start()
