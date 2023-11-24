import json
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG

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
