from flask import Flask
import time

from easysmart.device.device_define import get_device_define
import logging
from easysmart.manager import Manager
app = Flask(__name__)

m = None
# m = Manager()
# m.loop_start()

@app.route('/')
def index():
    msg = ''
    for k, v in m.devices.items():
        msg += f'mac:{k}\t type:{v.device_type}\n'
    return msg

@app.route('/t')
def t():
    devices = m.get_device(device_type='virtual_device')
    if len(devices) == 0:
        return 'no virtual_device'
    device = devices[0]
    device.set_property('test1', 1)
    time.sleep(0.2)
    msg = f'test1:{getattr(device, "test1", None)}'
    return msg

@app.route('/hello')
def hello():
    return 'hello'

if __name__ == "__main__":
    app.run(port=2020, host="127.0.0.1", debug=True)
