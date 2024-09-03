import copy
import logging

DEVICES_DEFINE = {}

DEVICES_DEFINE['base_device'] = {
    "parent": "",
    "properties": {
        "device_type": {
            "value": "base_device",
            "writable": 0
        }
    },
    "actions": {

    }
}

DEVICES_DEFINE['DIANJI'] = {
    "parent": "base_device",
    "properties": {
        "power": {
            "type": "int",
            "name": "当前电击强度"
        },
        "delay": {
            "type": "int",
            "min": 1,
            "max": 100000,
            "name": "电击间隔ms"
        }
    },
    "actions": {
    },
    "name": "电击器"
}

DEVICES_DEFINE['QTZ01'] = {
    "parent": "base_device",
    "properties": {
        "distance": {
            "type": "float",
            "name": "当前距离",
            "writable": False
        },
        "report_delay_ms": {
            "type": "int",
            "min": 1,
            "max": 100000,
            "name": "汇报间隔"
        }
    },
    "actions": {
    },
    "name": "擎天柱1号"
}

DEVICES_DEFINE['TD01'] = {
    "parent": "base_device",
    "properties": {
        "power1": {
            "type": "int",
            "min": 0,
            "max": 255,
            "name": "1号跳蛋强度"
        },
        "power2": {
            "type": "int",
            "min": 0,
            "max": 255,
            "name": "2号跳蛋强度"
        }
    },
    "actions": {
    },
    "name": "跳弹01"
}


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
        for k, v in define.items():
            if k in ['properties', 'actions']: continue
            device_define[k] = v
    return device_define


def _get_device_define(device_type):
    logging.info(f'get device define {device_type}')
    return copy.deepcopy(DEVICES_DEFINE.get(device_type))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    get_device_define('QTZ01')
    # get_device_define('base_device')
