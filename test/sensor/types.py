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
import cc_lib


logger = root_logger.getChild(__name__.split(".", 1)[-1].rsplit(".", 1)[0])


class PushReading(cc_lib.types.Service):
    local_id = "pushReading"

    @staticmethod
    def task(value, timestamp):
        return {
            "time": timestamp,
            "unit": "kWh",
            "value": value
        }


class TestSensor(cc_lib.types.Device):
    device_type_id = config.Senergy.dt_test_sensor
    services = (PushReading, )

    def __init__(self, id: str, name: str, enabled: bool):
        self.id = id
        self.name = name
        self.enabled = enabled

    def getService(self, srv_handler: str, *args, **kwargs):
        service = super().getService(srv_handler)
        return service.task(*args, **kwargs)
