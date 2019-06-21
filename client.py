import cc_lib, logging, random, json, datetime, time


logger = cc_lib.logger.getLogger('test-client')
logger.setLevel(logging.INFO)


class PushReading(cc_lib.types.SensorService):
    uri = "iot#995f438d-7425-497b-8c23-6a29394a6a52"
    description = "Push current meter reading"
    name = "Push counter"


class FerrarisOpticalSensorType(cc_lib.types.Device):
    uri = "iot#fd0e1327-d713-41da-adfb-e3853a71db3b"
    description = "Test Ferraris Sensor"
    services = {
        "detection": PushReading
    }

    def __init__(self, id, name):
        self.id = id
        self.name = name


ferraris_sensor = FerrarisOpticalSensorType("0058-2345", "Ferraris Sensor")


def on_connect(client: cc_lib.client.Client):
    try:
        client.connectDevice(ferraris_sensor, asynchronous=True)
    except cc_lib.client._exception.DeviceConnectError:
        pass


test_client = cc_lib.client.Client()
test_client.setConnectClbk(on_connect)
test_client.connect(reconnect=True)

time.sleep(5)

reading = random.random() * 100

while True:
    reading += random.random()
    msg = cc_lib.client.message.Message(
        json.dumps({"time": '{}Z'.format(datetime.datetime.utcnow().isoformat()), "unit": "kWh", "value": reading})
    )
    event = cc_lib.client.message.Envelope(ferraris_sensor, "detection", msg)
    logger.info("Sending:\n{}".format(event))
    test_client.emmitEvent(event, asynchronous=True)
    time.sleep(10)
