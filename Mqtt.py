# This class provides an interface for interacting with MQTT (Message Queuing Telemetry Transport) using the Paho MQTT library.
# It supports publishing and subscribing to MQTT topics.

import re
import logging
import queue
from typing import Callable
import paho.mqtt.client as mqtt
from paho.mqtt.client import connack_string

from PythonLib.Scheduler import Scheduler

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
        self.onChangeDict = {}
        self.onChangeDictStartTime = {}
        self.topicCallbackDict = {}
        self.startWithTopicCallbackDict = {}
        self.queue = queue.Queue()

        self.__setup()

    def __reset(self, payload: str) -> None:
        """
        Reset MQTT data.

        Args:
            payload (str): The payload received when resetting MQTT data.
        """
        self.onChangeDict = {}
        self.onChangeDictStartTime = {}
        logger.info("MQTT resetted")

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

            # Check if Callback with exact topic was registered
            callback = self.topicCallbackDict.get(topic)
            if callback:
                try:
                    callback(payload)
                except BaseException:
                    logging.exception('_3_')
            else:
                logger.debug("Topic %s has no registered callback", topic)

            # Check if Callback was registered with topic as starter
            for startWithTopic, startWithTopicCallback in self.startWithTopicCallbackDict.items():
                if topic.startswith(startWithTopic):
                    try:
                        startWithTopicCallback(topic, payload)
                    except BaseException:
                        logging.exception('_2_')

    def __on_connect(self, client, userdata, flags, rc) -> None:
        logger.debug("on_connect: %s", connack_string(rc))

    def __on_disconnect(self, client, userdata, rc) -> None:
        logger.debug("on_disconnect %s %i", connack_string(rc), rc)

    def __setup(self) -> None:
        """
        Initialize the MQTT client and set up necessary configurations.
        """
        self.onChangeDict = {}
        self.onChangeDictStartTime = {}
        self.mqttClient.connect(self.hostname, self.port)
        self.mqttClient.on_message = self.__on_message
        self.mqttClient.on_connect = self.__on_connect
        self.mqttClient.on_disconnect = self.__on_disconnect

        self.mqttClient.enable_logger(logger)

        # Register a service API for MQTT to reset persistent data
        self.subscribe('mqtt/reset', self.__reset)

        # Start a thread for the Paho MQTT client
        self.mqttClient.loop_start()

    def loop(self) -> None:
        """
        Perform cyclic jobs, processing all received data in the same context as the rest of the application (no multithreading).
        """
        self.__dispatchMessages()

    def publish(self, topic: str, payload: str, qos: int = 0) -> None:
        """
        Publish data to an MQTT topic.

        Args:
            topic (str): The topic to publish to (rootTopic/topic).
            payload (str): The payload to publish.
        """
        topic = self.rootTopic + "/" + re.sub(r'\s+', '_', topic)
        self.publishIndependentTopic(topic, payload, qos)

    def publishIndependentTopic(self, topic: str, payload: str, qos: int = 0) -> None:
        """
        Publish data to an MQTT topic.

        Args:
            topic (str): The topic to publish to.
            payload (str): The payload to publish.
        """
        logger.debug("Publish: %s : %s", topic, payload)
        self.mqttClient.publish(topic, payload, qos)

    def publishOnChange(self, topic: str, payload: str, forceUpdateMs: int = 60000) -> None:
        """
        Publish data to an MQTT topic only if the payload has changed.

        Args:
            topic (str): The topic to publish to (rootTopic/topic).
            payload (str): The payload to publish.
        """
        topic = self.rootTopic + "/" + topic
        self.publishOnChangeIndependentTopic(topic, payload, forceUpdateMs)

    def publishOnChangeIndependentTopic(self, topic: str, payload: str, forceUpdateMs: int = 60000) -> None:
        """
        Publish data to an MQTT topic only if the payload has changed.

        Args:
            topic (str): The topic to publish to.
            payload (str): The payload to publish.
        """
        if self.onChangeDict.get(topic) != payload:
            # Payload changed, publish
            self.onChangeDict[topic] = payload
            self.onChangeDictStartTime[topic] = Scheduler.getMillis()
            self.publishIndependentTopic(topic, payload)
        else:
            # Payload not changed, but perhaps timeout is over
            if Scheduler.getMillis() - self.onChangeDictStartTime.get(topic, 0) > forceUpdateMs:
                # timeout is over
                self.onChangeDict[topic] = payload
                self.onChangeDictStartTime[topic] = Scheduler.getMillis()
                self.publishIndependentTopic(topic, payload)

    def subscribe(self, topic: str, callback: Callable[[str], None]) -> None:
        """
        Subscribe to an MQTT topic and specify a callback function to handle incoming messages.

        Args:
            topic (str): The topic to subscribe to (rootTopic/topic)
            callback (Callable[[str], None]): A callback function that accepts the message payload.
        """
        topic = self.rootTopic + "/" + topic
        self.subscribeIndependentTopic(topic, callback)

    def subscribeIndependentTopic(self, topic: str, callback: Callable[[str], None]) -> None:
        """
        Subscribe to an MQTT topic and specify a callback function to handle incoming messages.

        Args:
            topic (str): The topic to subscribe to
            callback (Callable[[str], None]): A callback function that accepts the message payload.
        """

        self.topicCallbackDict[topic] = callback
        self.mqttClient.subscribe(topic, qos=1)

    def getSubscriptionCatalog(self) -> list[str]:
        return list(self.topicCallbackDict.keys())

    def subscribeStartWithTopic(self, topic: str, callback: Callable[[str, str], None]) -> None:
        """
        Subscribe to all MQTT topic starting with topic and specify a callback function to handle incoming messages.

        Args:
            topic (str): The beginning of topic to subscribe to
            callback (Callable[[str,str], None]): A callback function that accepts the topic and the message payload.
        """

        self.startWithTopicCallbackDict[topic] = callback
        self.mqttClient.subscribe(topic + "#", qos=1)


class MQTTHandler(logging.Handler):

    def __init__(self, mqttClient: Mqtt, topic: str) -> None:
        super().__init__()
        self.mqtt = mqttClient
        self.topic = topic

    def emit(self, record):
        log_message = self.format(record)
        self.mqtt.publishIndependentTopic(self.topic, log_message)
