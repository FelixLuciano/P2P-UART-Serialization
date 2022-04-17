import math
from typing import Generator

from alive_progress import alive_bar

from lib.enlace import Enlace
from lib.package import *


class Data_stream:
    def __init__ (self, data:bytes=b''):
        self.data = data


    def __len__ (self):
        return math.ceil(len(self.data) / Data_package.MAX_PAYLOAD_SIZE)


    def encode(self) -> Generator[Data_package, None, None]:
        length = len(self)

        for index, step in enumerate(range(0, len(self.data), Data_package.MAX_PAYLOAD_SIZE), 1):
            payload = self.data[step:step+Data_package.MAX_PAYLOAD_SIZE]

            yield Data_package(length, index, payload)


    @staticmethod
    def decode (stream:list):
        data = b''.join([package.data for package in stream])

        return Data_stream(data)


    @staticmethod
    def request (enlace:Enlace, target:int, timeout:int=-1):
        buffer = []
        count = 1

        while True:
            try:
                request = Request_package.request(enlace, timeout, target=target)

                Response_package().submit(enlace)

                with alive_bar(request.length, title='Receiving') as bar:
                    response = Data_package.request(enlace, timeout, length=request.length, index=count)

                    buffer.append(response)
                    bar()

                    count += 1

                    if response.index == request.length:
                        break
                    break

            except Request_package.UnexpectedRequestException:
                pass

            except Enlace.TimeoutException as error:
                raise Data_stream.TimeoutException(error.time)

        return Data_stream.decode(buffer)


    def submit (self, enlace:Enlace, target:int=0, timeout:int=-1):
        try:
            length = len(self)

            Request_package(target, length).submit(enlace)

            response = Response_package.request(enlace, timeout)
            
            with alive_bar(length, title='Transmiting') as bar:
                for package in self.encode():
                    package.submit(enlace, timeout)
                    print('Success!')
                    bar()

        except Enlace.TimeoutException as error:
            raise Data_stream.TimeoutException(error.time)


    class TimeoutException (Enlace.TimeoutException):
        """Couldn't receive the stream requested within the timeout.
        """
        pass
