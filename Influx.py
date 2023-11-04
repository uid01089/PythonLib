from __future__ import annotations
import logging
from influxdb import InfluxDBClient

logger = logging.getLogger('Influx')

# https://influxdb-python.readthedocs.io/en/latest/examples.html#tutorials-basic


class Influx:
    def __init__(self, host: str, database: str) -> None:
        self.client = InfluxDBClient(host='koserver.parents', port=8086, database="Mqtt2Influx")
        self.database = database

    def createDatabase(self) -> Influx:
        self.client.create_database(self.database)

    def write(self, measurement: str, fields: dict) -> Influx:

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
