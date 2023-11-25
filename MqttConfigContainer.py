from json import JSONDecodeError
import logging
import pathlib
from typing import Callable
from PythonLib.JsonUtil import JsonUtil
from PythonLib.Mqtt import Mqtt


logger = logging.getLogger('MqttConfigContainer')


class MqttConfigContainer:
    def __init__(self, mqtt: Mqtt, configTopic: str, path: pathlib.Path, defaultConfig: dict = None) -> None:
        self.mqtt = mqtt
        self.configTopic = configTopic
        self.path = path
        self.config = {} if defaultConfig is None else defaultConfig
        self.subscriber = []

    def setup(self) -> None:
        # Load config file if existing
        if self.path.exists():
            self.config = JsonUtil.loadJson(self.path)

        # Subscribe config channel to receive new config
        self.mqtt.subscribeIndependentTopic(self.configTopic + "/set", self.__configReceived)

    def loop(self) -> None:
        # Publish current config
        self.mqtt.publishIndependentTopic(self.configTopic, self.getAsJsonStr())

    def subscribeToConfigChange(self, callback: Callable[[dict], None]) -> None:
        self.subscriber.append(callback)

        # Provide the existing config quite after registration
        callback(self.config)

    def save(self, config: dict) -> None:
        JsonUtil.saveJson(self.path, config)

    def getAsDict(self) -> dict:
        return self.config

    def getAsJsonStr(self) -> str:
        return JsonUtil.obj2Json(self.config)

    def __triggerAllSubscriber(self) -> None:
        for callback in self.subscriber:
            callback(self.config)

    def __configReceived(self, configAsJsonStr: str) -> None:
        try:
            self.config = JsonUtil.json2Obj(configAsJsonStr)

            self.mqtt.publishIndependentTopic(self.configTopic, self.getAsJsonStr())

            self.save(self.config)

            self.__triggerAllSubscriber()

        except JSONDecodeError:
            logging.exception("Received config not a json")
