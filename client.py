"""
   Copyright 2019 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


from test.configuration import config
from test.logger import root_logger
from test.device_manager import DeviceManager
from test.sensor.types import TestSensor
from test.sensor.handler import SensorHandler
from test.actuator.types import TestActuator
from test.actuator.handler import ActuatorHandler
import cc_lib, time, uuid


logger = root_logger.getChild(__name__)


device_manager = DeviceManager()


def on_connect(client: cc_lib.client.Client):
    devices = device_manager.devices
    for device in devices:
        try:
            if device.enabled:
                client.connectDevice(device, asynchronous=True)
        except cc_lib.client.DeviceConnectError:
            pass


connector_client = cc_lib.client.Client()
connector_client.setConnectClbk(on_connect)

if not config.Sensor.id:
    config.Sensor.id = uuid.uuid4()

sensor_device = TestSensor(str(config.Sensor.id), str(config.Sensor.name), config.Sensor.enable)
device_manager.add(sensor_device)

if not config.Actuator.id:
    config.Actuator.id = uuid.uuid4()

actuator_device = TestActuator(str(config.Actuator.id), str(config.Actuator.name), config.Actuator.enable)
device_manager.add(actuator_device)

sensor_handler = SensorHandler(sensor_device, connector_client)
actuator_handler = ActuatorHandler(actuator_device, connector_client)

if __name__ == '__main__':
    try:
        while True:
            try:
                connector_client.initHub()
                break
            except cc_lib.client.HubNotFoundError:
                pass
            except cc_lib.client.HubInitializationError:
                time.sleep(5)
        while True:
            try:
                for device in device_manager.devices:
                    connector_client.addDevice(device)
                break
            except cc_lib.client.DeviceAddError:
                time.sleep(5)
        while True:
            try:
                connector_client.syncHub(device_manager.devices)
                break
            except cc_lib.client.HubSyncError:
                time.sleep(5)
        connector_client.connect(reconnect=True)
        if config.Actuator.enable:
            actuator_handler.start()
        if config.Sensor.enable:
            sensor_handler.start()
        for handler in (actuator_handler, sensor_handler):
            if handler.is_alive():
                handler.join()
    except KeyboardInterrupt:
        print("\ninterrupted by user\n")
