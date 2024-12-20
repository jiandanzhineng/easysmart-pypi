import json
import logging
import time

from .device_define import get_device_define


class BaseDevice:

    def __init__(self, mac, device_type, mqtt_client):
        self.device_type = device_type
        self.mac = mac
        self.last_active_time = time.time()
        self.msg_id = 0
        self.mqtt_client = mqtt_client

        self.publish_topic = f'/drecv/{mac}'

        device_define = get_device_define(device_type)

        if device_define is None:
            # device_define = get_device_define('base_device')
            logging.warning(f'get_device_define error: {device_type}')
            # raise Exception(f'get_device_define error: {device_type}')
            self.properties = {}
            self.actions = {}
            self.name = device_type
        else:
            self.properties = device_define['properties']
            self.actions = device_define['actions']
            self.name = device_define['name']

    async def publish(self, data):
        data['msg_id'] = self.msg_id
        self.msg_id += 1
        payload = json.dumps(data)
        await self.mqtt_client.publish(self.publish_topic, payload=payload)
        # self.mqtt_client.publish(self.publish_topic, payload)

    async def get_property(self, property_name):
        data = {
            'method': 'get',
            'key': property_name,
        }
        await self.publish(data)

    async def set_property(self, property_name, value):
        if property_name not in self.properties:
            logging.warning(f'property {property_name} not in {self.mac}, 请自己注意输入数据格式')
        else:
            if self.properties[property_name]['type'] == 'int':
                value = int(value)
            elif self.properties[property_name]['type'] == 'float':
                value = float(value)
        data = {
            'method': 'set',
            'key': property_name,
            'value': value,
        }
        await self.publish(data)

    async def set_multi_properties(self, properties):
        data = {
            'method': 'update',
        }
        data.update(properties)
        await self.publish(data)

    def execute_action(self, action_name):
        ...

    def update(self, property_name, value):
        update_flag = False
        if property_name not in self.properties:
            logging.warning(f'property {property_name} not in {self.mac}')
        if not hasattr(self, property_name):
            # 如果没有这个属性，就创建一个
            update_flag = True
            setattr(self, property_name, value)
            self.properties[property_name] = {
                'type': 'unknown',
                'name': property_name,
            }
        else:
            # 如果有这个属性，就更新这个属性
            old_value = getattr(self, property_name)
            if old_value != value:
                update_flag = True
                setattr(self, property_name, value)
        if update_flag:
            print(f'update {self.mac}:{property_name}->{value}')
        self.last_active_time = time.time()

    def to_dict(self):
        return {
            'device_type': self.device_type,
            'mac': self.mac,
            'last_active_time': self.last_active_time,
            'properties': {k: getattr(self, k) if hasattr(self, k) else None for k in self.properties.keys()},
        }
