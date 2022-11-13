import paho.mqtt.client as mqtt
from typing import Callable
import re
import logging
import queue

# https://github.com/eclipse/paho.mqtt.python
# https://mntolia.com/mqtt-python-with-paho-mqtt-client/

logger = logging.getLogger('PythonLib.Mqtt')

class Mqtt:
    def __init__(self, hostName : str, rootTopic : str, mqttClient: mqtt.Client, port = 1883) -> None:
        self.hostname = hostName
        self.port = port
        self.mqttClient = mqttClient
        self.rootTopic = rootTopic
        self.onChangeDict = dict()
        self.topicCallbackDict = dict()
        self.queue = queue.Queue()
        
    def __reset(self, payload: str) -> None:

        self.onChangeDict = dict()
        logger.info(f'MQTT reseted')

    def __on_message(self, client, userdata, message):   
        """This operation is called by paho.mqtt in case a new subscribed message was received. 
            The data are then stored in an queue

        Args:
            client (_type_): _description_
            userdata (_type_): _description_
            message (_type_): class with topic, payload, qos, retain
        """
        
        payload = str(message.payload)
        topic = str(message.topic)
        self.queue.put((topic, payload))

    def __dispatchMessages(self) -> None:
        """Perform work on all received submitted messages
        """
        while not self.queue.empty():
            item = self.queue.get()
            topic = item[0]
            payload = item[1]
            callback = self.topicCallbackDict.get(topic)
            if callback:
                callback(payload)
            else:
                logger.error(f'Topic {topic} was no callback registered')


    def setup(self) -> None:
        """ Do needfull things to setup the Mqtt class. 
        """

        
        self.onChangeDict = dict()
        self.mqttClient.connect(self.hostname, self.port)
        self.mqttClient.on_message = self.__on_message

        # register service API for mqtt to reset the persistent data
        self.subscribe('mqtt/reset', self.__reset)
        
        # start threat for paho.mqtt.client
        self.mqttClient.loop_start()

    def loop(self) -> None:
        """ Perform cyclically jobs, in this case process all received data in the same context like the other application (no multithreading)
        """
        
        self.__dispatchMessages()


    def publish(self, topic: str, payload: str) -> None:

        """Publish data with topic and payload
        """
        
        topic = self.rootTopic + "/" + re.sub(r'\s+', '_',   topic) 
        
        logger.debug(f'Publish: {topic} : {payload}')

        self.mqttClient.publish(topic, payload)

    def publishOnChange(self, topic: str, payload: str) -> None:
        """Publish only if payload is changed

        Args:
            topic (str): topic to be published
            payload (str): payload to be published
        """
        
        if self.onChangeDict.get(topic) != payload:
            self.onChangeDict[topic] = payload
            self.publish(topic, payload)


    def subscribe(self, topic : str, callback: Callable[[str], None]) -> None:
        """subscribe on a topic

        Args:
            topic (str): _description_
            callback (function): function with on_message(client, userdata, message), whereas message a class with topic, payload, qos, retain
        """
        
        topic = self.rootTopic + "/" + topic
        self.topicCallbackDict[topic] = callback
        
        self.mqttClient.subscribe(self.rootTopic + "/" + topic, qos=1)
        #self.mqttClient.message_callback_add(self.rootTopic + "/" + topic, callback)
