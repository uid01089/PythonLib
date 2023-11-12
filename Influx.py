from __future__ import annotations
import logging
from influxdb import InfluxDBClient

from PythonLib.Scheduler import Scheduler

logger = logging.getLogger('Influx')

# https://influxdb-python.readthedocs.io/en/latest/examples.html#tutorials-basic


class Influx:
    def __init__(self, host: str, database: str) -> None:
        self.client = InfluxDBClient(host='koserver.parents', port=8086, database="Mqtt2Influx")
        self.database = database
        self.onChangeDict = {}
        self.onChangeDictStartTime = {}

    def createDatabase(self) -> Influx:
        self.client.create_database(self.database)

    def deleteDatabase(self) -> Influx:
        self.client.drop_database(self.database)

    def write(self, measurement: str, fields: dict) -> Influx:

        if len(fields) != 0:
            json_body = [
                {
                    "measurement": measurement,
                    "tags": {
                    },
                    "fields": fields
                }
            ]

            self.client.write_points(json_body)

        return self

    def writeOnChange(self, measurement: str, fields: dict, forceUpdateMs: int = 60000) -> Influx:
        dictToWrite = {}
        for topic, payload in fields.items():

            if self.onChangeDict.get(topic) != payload:
                # Payload changed, write
                self.onChangeDict[topic] = payload
                self.onChangeDictStartTime[topic] = Scheduler.getMillis()
                dictToWrite[topic] = payload
            else:
                # Payload not changed, but perhaps timeout is over
                if Scheduler.getMillis() - self.onChangeDictStartTime.get(topic, 0) > forceUpdateMs:
                    # timeout is over
                    self.onChangeDict[topic] = payload
                    self.onChangeDictStartTime[topic] = Scheduler.getMillis()
                    dictToWrite[topic] = payload

        return self.write(measurement, dictToWrite)
