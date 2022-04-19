import math
from typing import Generator
from logging import Logger

from alive_progress import alive_bar

from lib.enlace import Enlace
from lib.header import Header
from lib.package import *


class Bytes_stream:
    MAX_DATA_SIZE = Data_package.MAX_PAYLOAD_SIZE * 255


    def __init__ (self, data:bytes=b''):
        if len(data) > Bytes_stream.MAX_DATA_SIZE:
            raise Bytes_stream.ExcededSizeLimitException()

        self.data = data


    def __len__ (self):
        return math.ceil(len(self.data) / Data_package.MAX_PAYLOAD_SIZE)


    def encode(self) -> Generator[Data_package, None, None]:
        length = len(self)

        for index, step in enumerate(range(0, len(self.data), Data_package.MAX_PAYLOAD_SIZE), 1):
            payload = self.data[step:step+Data_package.MAX_PAYLOAD_SIZE]

            yield Data_package(length, index, payload)


    @staticmethod
    def decode (stream:list[Data_package]):
        data = b''.join([package.data for package in stream])

        return Bytes_stream(data)


    @staticmethod
    def request (enlace:Enlace, target:int, timeout:int=-1, logger:Logger=None):
        buffer = []
        count = 1

        try:
            request = Request_package.request(enlace, timeout, logger, target=target)

            Response_package().submit(enlace, logger)

            if logger == None:
                with alive_bar(request.length, title='Receiving', enrich_print=False) as bar:
                    while True:
                        response = Data_package.request(enlace, timeout, logger, length=request.length, index=count)

                        buffer.append(response)
                        bar()

                        if response.index == request.length:
                            break

                        count += 1

            else:
                while True:
                    response = Data_package.request(enlace, timeout, logger, length=request.length, index=count)

                    buffer.append(response)

                    if response.index == request.length:
                        break

                    count += 1

        except Request_package.UnexpectedRequestException:
            pass

        except Enlace.TimeoutException as error:
            raise Bytes_stream.TimeoutException(error.time)

        return Bytes_stream.decode(buffer)


    def submit (self, enlace:Enlace, target:int=0, timeout:int=-1, logger:Logger=None):
        try:
            length = len(self)

            Request_package(target, length).submit(enlace, logger)

            response = Response_package.request(enlace, timeout, logger)
            
            if logger == None:
                with alive_bar(length, title='Transmiting', enrich_print=False) as bar:
                    for package in self.encode():
                        package.submit(enlace, timeout, logger)
                        bar()

            else:
                for package in self.encode():
                    package.submit(enlace, timeout, logger)

        except Enlace.TimeoutException as error:
            raise Bytes_stream.TimeoutException(error.time)


    class ExcededSizeLimitException (Header.ExcededSizeLimitException):
        """Data size exceed limit.
        """
        pass


    class TimeoutException (Enlace.TimeoutException):
        """Couldn't receive the stream requested within the timeout.
        """
        pass
