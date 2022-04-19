import json
from typing import Generator

from lib.stream.Bytes import Bytes_stream
from lib.package import Data_package


class Data_stream (Bytes_stream):
    def __init__ (self, data:any):
        super().__init__(data)


    def encode(self) -> Generator[Data_package, None, None]:
        data = json.dumps(self.data).encode()
        length = len(self)

        for index, step in enumerate(range(0, len(data), Data_package.MAX_PAYLOAD_SIZE), 1):
            payload = data[step:step+Data_package.MAX_PAYLOAD_SIZE]

            yield Data_package(length, index, payload)


    @staticmethod
    def decode (stream:list[Data_package]):
        data_bytes = b''.join([package.data for package in stream])
        data = json.loads(data_bytes)

        return Bytes_stream(data)
