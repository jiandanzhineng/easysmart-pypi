import requests
import json
import os
import pathlib
import logging

DEVICE_DEFINE_PATH = r'devices_define'


def get_device_define(device_type):
    defines = []
    device_define = _get_device_define(device_type)
    defines.append(device_define)
    while device_define and device_define.get('parent'):
        device_define = _get_device_define(device_define['parent'])
        defines.append(device_define)
    defines.reverse()
    for define in defines:
        if define is None: continue
        device_define['properties'].update(define['properties'])
        device_define['actions'].update(define['actions'])
        for k,v in define.items():
            if k in ['properties','actions']: continue
            device_define[k] = v
    return device_define


def _get_device_define(device_type):
    logging.info(f'get device define {device_type}')
    # check if dir devices_define exists
    if not os.path.exists(DEVICE_DEFINE_PATH):
        logging.info(f'create devices_define dir')
        os.makedirs(DEVICE_DEFINE_PATH)
    json_file = f'{DEVICE_DEFINE_PATH}/{device_type}.json'
    print(f'get device define from {json_file}')
    if os.path.exists(json_file):
        logging.info(f'get device define from local')
        with open(json_file, 'r', encoding='utf-8') as f:
            device_define = json.load(f)
            return device_define
    else:
        # download device define from server and save it to local
        # url: http://device.easysmart.top/device_define/{device_type}.json
        url = f'http://device.easysmart.top/device_define/{device_type}.json'
        logging.info(f'get device define from server：{url}')
        try:
            r = requests.get(url)
            if r.status_code != 200:
                logging.warning(f'get device define {device_type} failed {r.status_code}')
                return
            device_define = r.json()
        except Exception as e:
            logging.warning(f'get device define {device_type} failed {e}')
            return
        with open(f'{DEVICE_DEFINE_PATH}/{device_type}.json', 'w', encoding='utf-8') as f:
            json.dump(device_define, f)
        return device_define


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    get_device_define('QTZ01')
    # get_device_define('base_device')
