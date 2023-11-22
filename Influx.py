from __future__ import annotations
import logging
from influxdb import InfluxDBClient

from PythonLib.Scheduler import Scheduler

logger = logging.getLogger('Influx')

# https://influxdb-python.readthedocs.io/en/latest/examples.html#tutorials-basic


class RetentionPolicy:
    # https://archive.docs.influxdata.com/influxdb/v1.0/query_language/database_management/#retention-policy-management

    '''
        Durations such as 1h, 90m, 12h, 7d, and 4w, are all supported
        and mean 1 hour, 90 minutes, 12 hours, 7 day, and 4 weeks,
        respectively. For infinite retention, meaning the data will
        never be deleted, use 'INF' for duration.
        The minimum retention period is 1 hour.
    '''

    def __init__(self, influxDBClient: InfluxDBClient, retentionStr: str) -> None:
        self.retentionStr = retentionStr
        self.influxDBClient = influxDBClient
        self.influxDBClient.create_retention_policy(self.retentionStr, self.retentionStr, "1")

    def getName(self) -> str:
        return self.retentionStr


class Influx:
    def __init__(self, host: str, database: str) -> None:
        self.client = InfluxDBClient(host=host, port=8086, database=database)
        self.database = database
        self.onChangeDict = {}
        self.onChangeDictStartTime = {}

    def createRetentionPolicy(self, retentionStr: str) -> RetentionPolicy:
        return RetentionPolicy(self.client, retentionStr)

    def createDatabase(self) -> Influx:
        self.client.create_database(self.database)

    def deleteDatabase(self) -> Influx:
        self.client.drop_database(self.database)

    def write(self, measurement: str, fields: dict, retentionPolicy: str = None) -> Influx:

        if len(fields) != 0:
            json_body = [
                {
                    "measurement": measurement,
                    "tags": {
                    },
                    "fields": fields
                }
            ]

            self.client.write_points(json_body, retention_policy=retentionPolicy)

        return self

    def writeOnChange(self, measurement: str, fields: dict, forceUpdateMs: int = 60000, retentionPolicy: str = None) -> Influx:
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

        return self.write(measurement, dictToWrite, retentionPolicy=retentionPolicy)
