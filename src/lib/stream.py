import math

from lib.thread import Thread
from lib.commands import Commands
from lib.header import Header
from lib.package import Package


class Stream:
    PACKAGE_SIZE = 128

    def __init__ (self, type_:str, data:bytes):
        self.type = type_
        self.data = data


    def encode(self):
        payloadSize = self.PACKAGE_SIZE - Header.SIZE - len(Package.EOP)
        length = math.ceil(len(self.data) / payloadSize)
        stream = []

        for index, step in enumerate(range(0, len(self.data), payloadSize)):
            payload = self.data[step:step+payloadSize]
            package = Package(self.type, index, length, payload)

            stream.append(package)

        return stream


    @classmethod
    def decode (cls, stream:list):
        type_ = stream[0].type
        data = b''.join([package.data for package in stream])

        return cls(
            type_ = type_,
            data = data
        )


    @classmethod
    def request (cls, thread:Thread, timeout:int=-1):
        stream = []

        while True:
            request = Package.request(thread, index=len(stream), timeout=timeout)

            if request != None:
                stream.append(request)
                Package(type_='error').submit(thread)

                if len(stream) == request.length:
                    break
            else:
                Package(type_='error').submit(thread)
                # thread.clear()

        Package(type_='success').submit(thread)

        return cls.decode(stream)


    def submit (self, thread:Thread, timeout:int=-1):
        ended = False

        while not ended:
            for package in self.encode():
                done = False

                while not done:
                    package.submit(thread)

                    response = Package.request(thread, timeout=timeout)

                    if response.type == 'success':
                        done = True
                    else:
                        tryAgain = input('Sending failed. Try again? Y/N ')

                        if tryAgain.lower() not in ('y', 'yes'):
                            done = True

            response = Package.request(thread, timeout=timeout)

            if response.type == 'success':
                ended = True
            else:
                tryAgain = input('Sending failed. Try again? Y/N ')

                if tryAgain.lower() not in ('y', 'yes'):
                    ended = True
