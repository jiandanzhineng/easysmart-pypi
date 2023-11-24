from easysmart.device.virtual_device.virtual_base_device import VirtualDevice
import logging
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    device = VirtualDevice('123456789012')
    device.run()
