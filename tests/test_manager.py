import os

import pytest

from easysmart import Manager


def test_control():

    def on_connect(client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        # client.subscribe(topic, 0)

    curPath = os.path.abspath(os.path.dirname(__file__))
    print(curPath)
    m = Manager()
