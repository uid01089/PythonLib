import asyncio
import logging
import re
from typing import Callable
import paho.mqtt.client as mqtt

from PythonLib.Scheduler import Scheduler
from PythonLib.Mqtt import Mqtt

# https://pypi.org/project/aiomqtt/

logger = logging.getLogger('PythonLib.AsyncMqtt')


class AsyncMqtt:
    def __init__(self, hostName: str, rootTopic: str, mqttClient: mqtt.Client, port: object = 1883) -> None:
        """
        Initialize the Mqtt class.

        Args:
            hostName (str): The MQTT broker's hostname.
            rootTopic (str): The root topic for MQTT communications.
            mqttClient (mqtt.Client): The Paho MQTT client instance to use.
            port (int, optional): The MQTT broker's port (default is 1883).
        """
        self.mqttClient = Mqtt(hostName, rootTopic, mqttClient, port)

        self.task = None

    async def connectAndRun(self) -> None:

        async def fct():
            while True:
                self.mqttClient.loop()
                await asyncio.sleep(0.1)

        self.task = asyncio.create_task(fct())

    async def publish(self, topic: str, payload: str, qos: int = 0) -> None:
        self.mqttClient.publish(topic, payload, qos)

    async def publishIndependentTopic(self, topic: str, payload: str, qos: int = 0) -> None:
        self.mqttClient.publishIndependentTopic(topic, payload, qos)

    async def publishOnChange(self, topic: str, payload: str, forceUpdateMs: int = 60000) -> None:
        self.mqttClient.publishOnChange(topic, payload, forceUpdateMs)

    async def publishOnChangeIndependentTopic(self, topic: str, payload: str, forceUpdateMs: int = 60000) -> None:
        self.mqttClient.publishOnChangeIndependentTopic(topic, payload, forceUpdateMs)

    async def subscribe(self, topic: str, callback: Callable[[str], None]) -> None:
        self.mqttClient.subscribe(topic, callback)

    async def subscribeIndependentTopic(self, topic: str, callback: Callable[[str], None]) -> None:
        self.mqttClient.subscribeIndependentTopic(topic, callback)

    async def getSubscriptionCatalog(self) -> list[str]:
        return self.mqttClient.getSubscriptionCatalog()

    async def subscribeStartWithTopic(self, topic: str, callback: Callable[[str, str], None]) -> None:
        self.mqttClient.subscribeStartWithTopic(topic, callback)


class AsyncMQTTHandler(logging.Handler):

    def __init__(self, mqttClient: AsyncMqtt, topic: str) -> None:
        super().__init__()
        self.mqtt = mqttClient
        self.topic = topic
        self.background_tasks = set()

    def emit(self, record):
        log_message = self.format(record)

        task = asyncio.create_task(self.mqtt.publishIndependentTopic(self.topic, log_message))
        self.background_tasks.add(task)
        task.add_done_callback(self.background_tasks.remove)
