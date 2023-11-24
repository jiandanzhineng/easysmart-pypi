from easysmart.device.device_define import get_device_define
import logging

def test_device_define():
    get_device_define('virtual_device')
    get_device_define('base_device')
