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
import cc_lib, datetime


logger = root_logger.getChild(__name__.split(".", 1)[-1].rsplit(".", 1)[0])


class PrintTime(cc_lib.types.ActuatorService):
    uri = config.Senergy.st_print_time
    name = "Print Time"
    description = "Print time to local console."

    @staticmethod
    def task():
        logger.info("{}Z".format(datetime.datetime.utcnow().isoformat()))
        return {"status": 0}


class PrintValues(cc_lib.types.ActuatorService):
    uri = config.Senergy.st_print_values
    name = "Print Values"
    description = "Print values provided by user."

    @staticmethod
    def task(val_a: str, val_b: str):
        logger.info("val_a: '{}', val_b: '{}'".format(val_a, val_b))
        return {"status": 0}


class TestActuator(cc_lib.types.Device):
    uri = config.Senergy.dt_test_actuator
    description = "Device type for test actuator."
    services = {
        "printTime": PrintTime,
        "printValues": PrintValues
    }

    def __init__(self, id: str, name: str, enabled: bool):
        self.id = id
        self.name = name
        self.enabled = enabled

    def getService(self, srv_handler: str, *args, **kwargs):
        service = super().getService(srv_handler)
        return service.task(*args, **kwargs)
