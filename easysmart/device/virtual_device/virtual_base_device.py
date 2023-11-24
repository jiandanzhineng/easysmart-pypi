import json
import time

from easysmart.device.device_define import get_device_define
from easysmart.utils import on_log, on_connect, on_disconnect
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from paho.mqtt import client as mqtt

class VirtualDevice:
    device_type = 'virtual_device'

    def __init__(self, mac):
        self.power = 0
        self.mac = mac
        assert len(mac) == 12
        device_define = get_device_define(self.device_type)
        if device_define is None:
            raise Exception(f'get_device_define error: {self.device_type}')
        self.properties = device_define['properties']
        self.actions = device_define['actions']
        for property_name in self.properties:
            setattr(self, property_name, self.properties[property_name]['value'])
        self.publish_topic = f'/dpub/{self.mac}'

    def connect_mqtt(self):
        self.client_id = 'MQTT_DEVICE_' + self.mac
        self.client = mqtt.Client(self.client_id, protocol=mqtt.MQTTv311, clean_session=False)
        self.client.on_log = on_log
        self.client.on_connect = on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = on_disconnect
        while True:
            try:
                self.client.connect('mqttserver.local', 1883, 60)
                break
            except:
                print('mqtt connect error, retry...')
                time.sleep(1)
        self.client.loop_start()

        self.client.subscribe(f'/drecv/{self.mac}', 1)
        self.client.subscribe('/all', 1)

    def run(self):
        self.connect_mqtt()
        while True:
            self.report()
            time.sleep(10)


    def publish(self, payload, qos=0, retain=False, properties=None):
        return self.client.publish(self.publish_topic, payload, qos, retain, properties)

    def report(self):
        data = {}
        for property_name in self.properties:
            data[property_name] = getattr(self, property_name)
        self.publish(json.dumps(data))

    def update_property(self, property_name, msg_id=-1):
        '''
        example:
        {
            "method":	"update",
            "msg_id":	1,
            "key":	"power2",
            "value":	0
        }
        '''
        data = {
            'method': 'update',
            'msg_id': msg_id,
            'key': property_name,
            'value': getattr(self, property_name) if hasattr(self, property_name) else None,
        }
        self.publish(json.dumps(data))


    def on_message(self, client, userdata, msg):
        print('topic:' + msg.topic + ' ' + str(msg.payload))
        try:
            data = json.loads(msg.payload)
        except:
            data = str(msg.payload)
            print(f'json.loads error: {data}')
            return
        print(f'{data}')
        try:
            self.msg_process(msg, data)
        except Exception as e:
            print(f'on_message error: {e}\n{msg}\n{data}')

    def msg_process(self, msg, data):
        msg_id = data.get('msg_id', -1)
        method = data.get('method', '')
        if method == 'set':
            '''
            example:
            {
              "method": "set",
              "key":"power2",
              "value":0,
              "msg_id":1
            }
            '''
            key = data.get('key', '')
            if key not in self.properties:
                print(f'key not in properties: {key}')
                return
            if not self.properties[key].get('writable', True):
                self.publish_error(f'key not writable: {key}', msg_id)
                return
            value = data.get('value', '')
            setattr(self, key, value)
            self.update_property(key, msg_id)
        elif method == 'get':
            '''
            example:
            {
              "method": "get",
              "key":"power2",
              "msg_id":1
            }
            '''
            key = data.get('key', '')
            self.update_property(key, msg_id)

    def publish_error(self, msg, msg_id):
        data = {
            'method': 'error',
            'msg_id': msg_id,
            'msg': msg,
        }
        self.publish(json.dumps(data))


if __name__ == '__main__':
    device = VirtualDevice('123456789012')
    device.run()
