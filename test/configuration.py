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


from simple_conf import configuration, section
from os import getcwd


@configuration
class TestConf:

    @section
    class Actuator:
        enable = False
        name = "Test Actuator"
        id = None

    @section
    class Sensor:
        enable = False
        name = "Test Sensor"
        id = None
        rate = 10

    @section
    class Senergy:
        dt_test_actuator = None
        dt_test_sensor = None
        st_print_time = None
        st_print_values = None
        st_push_reading = None

    @section
    class Logger:
        level = "info"


config = TestConf('test.conf', getcwd())


if not all(
        (
                str(config.Actuator.enable),
                config.Actuator.name,
                config.Actuator.id,
                str(config.Sensor.enable),
                config.Sensor.name,
                config.Sensor.id,
                config.Logger.level
        )
):
    exit('Please provide information for test actuator and sensor')


if not all(
        (
                config.Senergy.dt_test_actuator,
                config.Senergy.dt_test_sensor,
                config.Senergy.st_print_time,
                config.Senergy.st_push_reading
        )
):
    exit('Please provide a SENERGY device and service types')