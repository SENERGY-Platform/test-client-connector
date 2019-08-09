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


from ..configuration import config
from ..logger import root_logger
from .types import TestSensor
import random, threading, cc_lib, json, datetime, time


logger = root_logger.getChild(__name__.split(".", 1)[-1])


class SensorHandler(threading.Thread):
    def __init__(self, device: TestSensor, client: cc_lib.client.Client):
        super().__init__(name="sensor-{}".format(device.id), daemon=True)
        self.__device = device
        self.__client = client
        self.__reading = random.random() * 100

    def run(self) -> None:
        logger.info("starting sensor handler for '{}'".format(self.__device.id))
        msg = cc_lib.client.message.Message(str())
        srv = "pushReading"
        while True:
            self.__reading += random.random()
            payload = self.__device.getService(
                srv,
                value=self.__reading,
                timestamp='{}Z'.format(datetime.datetime.utcnow().isoformat())
            )
            msg.data = json.dumps(payload)
            event = cc_lib.client.message.EventEnvelope(self.__device, srv, msg)
            logger.info("sending event: '{}' - '{}Z'".format(
                event.correlation_id,
                datetime.datetime.utcnow().isoformat()
            ))
            logger.debug(event)
            self.__client.emmitEvent(event, asynchronous=True)
            time.sleep(config.Sensor.rate)
