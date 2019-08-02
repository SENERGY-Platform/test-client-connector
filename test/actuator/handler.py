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


from ..logger import root_logger
from .types import TestActuator
import threading, cc_lib, json


logger = root_logger.getChild(__name__.split(".", 1)[-1])


class ActuatorHandler(threading.Thread):
    def __init__(self, device: TestActuator, client: cc_lib.client.Client):
        super().__init__(name="actuator-{}".format(device.id), daemon=True)
        self.__device = device
        self.__client = client

    def run(self) -> None:
        logger.info("starting actuator handler for '{}'".format(self.__device.id))
        while True:
            command = self.__client.receiveCommand()
            logger.debug("received:\n'{}'".format(command))
            try:
                if command.message.data:
                    device_resp = self.__device.getService(command.service_uri, **json.loads(command.message.data))
                else:
                    device_resp = self.__device.getService(command.service_uri)
                resp = cc_lib.client.message.Message(json.dumps(device_resp))
            except json.JSONDecodeError as ex:
                logger.error("{}: could not parse command data - {}".format(self.name, ex))
                resp = cc_lib.client.message.Message(json.dumps({"status": 1}))
            except TypeError as ex:
                logger.error("{}: could not parse command response data - {}".format(self.name, ex))
                resp = cc_lib.client.message.Message(json.dumps({"status": 1}))
            command.message = resp
            logger.debug("sending response:\n'{}'".format(command))
            self.__client.sendResponse(command, asynchronous=True)
