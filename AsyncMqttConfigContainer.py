from json import JSONDecodeError
import logging
import pathlib
from typing import Callable
from PythonLib.JsonUtil import JsonUtil
from PythonLib.AsyncMqtt import AsyncMqtt


logger = logging.getLogger('PythonLib.AsyncMqttConfigContainer')


class AsyncMqttConfigContainer:
    def __init__(self, mqtt: AsyncMqtt, configTopic: str, path: pathlib.Path, defaultConfig: dict = None) -> None:
        self.mqtt = mqtt
        self.configTopic = configTopic
        self.path = path
        self.config = {} if defaultConfig is None else defaultConfig
        self.subscriber = []

    async def setup(self) -> None:
        # Load config file if existing
        if self.path.exists():
            self.config = JsonUtil.loadJson(self.path)

        # Subscribe config channel to receive new config
        await self.mqtt.subscribeIndependentTopic(self.configTopic + "/set", self.__configReceived)

    async def loop(self) -> None:
        # Publish current config
        await self.mqtt.publishIndependentTopic(self.configTopic, await self.getAsJsonStr())

    async def subscribeToConfigChange(self, callback: Callable[[dict], None]) -> None:
        self.subscriber.append(callback)

        # Provide the existing config quite after registration
        await callback(self.config)

    async def save(self, config: dict) -> None:
        JsonUtil.saveJson(self.path, config)

    async def getAsDict(self) -> dict:
        return self.config

    async def getAsJsonStr(self) -> str:
        return JsonUtil.obj2Json(self.config)

    async def __triggerAllSubscriber(self) -> None:
        for callback in self.subscriber:
            await callback(self.config)

    async def __configReceived(self, configAsJsonStr: str) -> None:
        try:
            self.config = JsonUtil.json2Obj(configAsJsonStr)

            await self.mqtt.publishIndependentTopic(self.configTopic, await self.getAsJsonStr())

            await self.save(self.config)

            await self.__triggerAllSubscriber()

        except JSONDecodeError:
            logging.exception("Received config not a json")
