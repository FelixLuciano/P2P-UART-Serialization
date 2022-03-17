import math

from lib.thread import Thread
from lib.header import Header
from lib.package import Package


class Stream:
    PACKAGE_SIZE = 128


    def __init__ (self, type_:str='data', data:bytes=b''):
        self.type = type_
        self.data = data


    def encode(self):
        payloadSize = self.PACKAGE_SIZE - Header.SIZE - len(Package.EOP)
        length = math.ceil(len(self.data) / payloadSize)

        for index, step in enumerate(range(0, len(self.data), payloadSize)):
            payload = self.data[step:step+payloadSize]
            package = Package(self.type, index, length, payload)

            yield package


    @classmethod
    def decode (cls, stream:list):
        type_ = stream[0].type
        data = b''.join([package.data for package in stream])

        return cls(
            type_ = type_,
            data = data
        )


    @classmethod
    def request (cls, thread:Thread, type_:str=None, length:int=None, timeout:int=-1):
        buffer = []

        while True:
            bufferLen = len(buffer)
            nextIndex = buffer[-1].index + 1 if bufferLen > 0 else 0
            nextType = buffer[-1].type if nextIndex > 0 else type_
            nextLength = buffer[-1].length if bufferLen > 0 else length
            request = Package.request(thread, type_=nextType, index=nextIndex, length=nextLength, timeout=timeout)

            buffer.append(request)

            if bufferLen + 1 == request.length:
                break

        Package(type_='success').submit(thread=thread, timeout=timeout)

        return cls.decode(buffer)


    def submit (self, thread:Thread, timeout:int=-1):
        while True:
            for package in self.encode():
                package.submit(thread, timeout=timeout)

            success, done = Package.getSuccessDone(
                thread=thread,
                message=f'Failed do submit {self.type} stream.',
                timeout=timeout
            )

            if success and done:
                break
            else:
                continue
