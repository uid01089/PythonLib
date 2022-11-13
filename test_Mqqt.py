from PythonLib.Mqtt import Mqtt

class paoMqttClient():
    def __init__(self, clientName: str) -> None:
        pass

    def connect(self, hostname: str, port: int) -> None:
        self.hostname = hostname
        self.port = port

    def publish(self, topic:str, payload:str) -> None:
        self.topic = topic
        self.payload = payload


def test1() -> None:
    poaClient = paoMqttClient("TestClient")
    mqttClient = Mqtt("koserver.parents", "heizung", poaClient)
    mqttClient.setup()

    assert poaClient.hostname == "koserver.parents"
    assert poaClient.port == 1883
    
def test2() -> None:
    poaClient = paoMqttClient("TestClient")
    mqttClient = Mqtt("koserver.parents", "heizung", poaClient)
    mqttClient.setup()
    mqttClient.publish("Hallo test/blo /blo", "wert wert")

    assert poaClient.topic == "Hallo_test/blo_/blo"
    assert poaClient.payload == "wert wert"

def test3() -> None:
    poaClient = paoMqttClient("TestClient")
    mqttClient = Mqtt("koserver.parents", "heizung", poaClient)
    mqttClient.setup()
    mqttClient.publishOnChange("Hallo test/blo /blo", "wert wert")

    assert poaClient.topic == "Hallo_test/blo_/blo"
    assert poaClient.payload == "wert wert"

    mqttClient.publishOnChange("Hallo test/blo /blo", "wert1")
    assert poaClient.topic == "Hallo_test/blo_/blo"
    assert poaClient.payload == "wert1"