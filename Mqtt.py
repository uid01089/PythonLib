# This class provides an interface for interacting with MQTT (Message Queuing Telemetry Transport) using the Paho MQTT library.
# It supports publishing and subscribing to MQTT topics.

import re
import logging
import queue
from typing import Callable
import paho.mqtt.client as mqtt

# https://github.com/eclipse/paho.mqtt.python
# https://mntolia.com/mqtt-python-with-paho-mqtt-client/

logger = logging.getLogger('PythonLib.Mqtt')


class Mqtt:
    def __init__(self, hostName: str, rootTopic: str, mqttClient: mqtt.Client, port: object = 1883) -> None:
        """
        Initialize the Mqtt class.

        Args:
            hostName (str): The MQTT broker's hostname.
            rootTopic (str): The root topic for MQTT communications.
            mqttClient (mqtt.Client): The Paho MQTT client instance to use.
            port (int, optional): The MQTT broker's port (default is 1883).
        """
        self.hostname = hostName
        self.port = port
        self.mqttClient = mqttClient
        self.rootTopic = rootTopic
        self.onChangeDict = dict()
        self.topicCallbackDict = dict()
        self.queue = queue.Queue()

        self.__setup()

    def __reset(self, payload: str) -> None:
        """
        Reset MQTT data.

        Args:
            payload (str): The payload received when resetting MQTT data.
        """
        self.onChangeDict = dict()
        logger.info(f'MQTT resetted')

    def __on_message(self, client, userdata, message):
        """
        Handle incoming MQTT messages.

        Args:
            client: The MQTT client instance.
            userdata: User data (not used in this implementation).
            message: A message object containing topic, payload, qos, and retain.
        """
        payload = message.payload.decode("utf-8")
        topic = str(message.topic)
        self.queue.put((topic, payload))

    def __dispatchMessages(self) -> None:
        """
        Process all received messages and invoke corresponding callbacks.
        """
        while not self.queue.empty():
            item = self.queue.get()
            topic = item[0]
            payload = item[1]
            callback = self.topicCallbackDict.get(topic)
            if callback:
                callback(payload)
            else:
                logger.error(f'Topic {topic} has no registered callback')

    def __setup(self) -> None:
        """
        Initialize the MQTT client and set up necessary configurations.
        """
        self.onChangeDict = dict()
        self.mqttClient.connect(self.hostname, self.port)
        self.mqttClient.on_message = self.__on_message

        # Register a service API for MQTT to reset persistent data
        self.subscribe('mqtt/reset', self.__reset)

        # Start a thread for the Paho MQTT client
        self.mqttClient.loop_start()

    def loop(self) -> None:
        """
        Perform cyclic jobs, processing all received data in the same context as the rest of the application (no multithreading).
        """
        self.__dispatchMessages()

    def publish(self, topic: str, payload: str) -> None:
        """
        Publish data to an MQTT topic.

        Args:
            topic (str): The topic to publish to.
            payload (str): The payload to publish.
        """
        topic = self.rootTopic + "/" + re.sub(r'\s+', '_', topic)

        logger.debug(f'Publish: {topic} : {payload}')

        self.mqttClient.publish(topic, payload)

    def publishOnChange(self, topic: str, payload: str) -> None:
        """
        Publish data to an MQTT topic only if the payload has changed.

        Args:
            topic (str): The topic to publish to.
            payload (str): The payload to publish.
        """
        if self.onChangeDict.get(topic) != payload:
            self.onChangeDict[topic] = payload
            self.publish(topic, payload)

    def subscribe(self, topic: str, callback: Callable[[str], None]) -> None:
        """
        Subscribe to an MQTT topic and specify a callback function to handle incoming messages.

        Args:
            topic (str): The topic to subscribe to.
            callback (Callable[[str], None]): A callback function that accepts the message payload.
        """
        topic = self.rootTopic + "/" + topic
        self.topicCallbackDict[topic] = callback

        self.mqttClient.subscribe(topic, qos=1)
