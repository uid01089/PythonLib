import logging
from time import sleep
import paho.mqtt.client as pahoMqtt
from PythonLib.Mqtt import Mqtt


class paoMqttClient():
    def __init__(self, clientName: str) -> None:
        pass

    def connect(self, hostname: str, port: int) -> None:
        self.hostname = hostname
        self.port = port

    def publish(self, topic: str, payload: str) -> None:
        self.topic = topic
        self.payload = payload

    def subscribe(self, topic, qos=0, options=None, properties=None):
        pass

    def loop_start(self) -> None:
        pass


def test1() -> None:
    poaClient = paoMqttClient("TestClient")
    mqttClient = Mqtt("koserver.parents", "heizung", poaClient)

    assert poaClient.hostname == "koserver.parents"
    assert poaClient.port == 1883


def test2() -> None:
    poaClient = paoMqttClient("TestClient")
    mqttClient = Mqtt("koserver.parents", "heizung", poaClient)

    mqttClient.publish("Hallo test/blo /blo", "wert wert")

    assert poaClient.topic == "heizung/Hallo_test/blo_/blo"
    assert poaClient.payload == "wert wert"


def test3() -> None:
    poaClient = paoMqttClient("TestClient")
    mqttClient = Mqtt("koserver.parents", "heizung", poaClient)
    mqttClient.publishOnChange("Hallo test/blo /blo", "wert wert")

    assert poaClient.topic == "heizung/Hallo_test/blo_/blo"
    assert poaClient.payload == "wert wert"

    mqttClient.publishOnChange("Hallo test/blo /blo", "wert1")
    assert poaClient.topic == "heizung/Hallo_test/blo_/blo"
    assert poaClient.payload == "wert1"


mqttReceived = ""


class Receiver:

    def __init__(self) -> None:
        self.mqttReceived = ""

    def fctReceived(self, payload: str) -> None:
        self.mqttReceived = payload

    def getReceived(self) -> str:
        return self.mqttReceived


def test4() -> None:
    logging.basicConfig(level=logging.DEBUG)
    receiver = Receiver()
    mqttClient = Mqtt("koserver.iot", "heizungsTest", pahoMqtt.Client("Developer"))
    mqttClient.subscribe("test", receiver.fctReceived)
    mqttClient.publish("test", "hallo")
    mqttClient.loop()
    sleep(10)
    mqttClient.loop()
    assert receiver.getReceived() == "hallo"
