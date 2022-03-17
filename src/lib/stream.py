import math

from alive_progress import alive_bar

from lib.thread import Thread
from lib.header import Header
from lib.package import Package


class Stream:
    PACKAGE_SIZE = 128
    PAYLOAD_SIZE = PACKAGE_SIZE - Header.SIZE - len(Package.EOP)


    def __init__ (self, type_:str='data', data:bytes=b''):
        self.type = type_
        self.data = data


    def __len__ (self):
        return math.ceil(len(self.data) / self.PAYLOAD_SIZE)


    def encode(self):
        for index, step in enumerate(range(0, len(self.data), self.PAYLOAD_SIZE)):
            payload = self.data[step:step+self.PAYLOAD_SIZE]
            package = Package(self.type, index, len(self), payload)

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

        with alive_bar(title='Receiving', manual=True) as bar:
            while True:
                bufferLen = len(buffer)
                nextIndex = buffer[-1].index + 1 if bufferLen > 0 else 0
                nextType = buffer[-1].type if nextIndex > 0 else type_
                nextLength = buffer[-1].length if bufferLen > 0 else length
                response = Package.request(thread, type_=nextType, index=nextIndex, length=nextLength, timeout=timeout)

                if response.type != 'error':
                    buffer.append(response)
                    bar((response.index + 1) / response.length)

                    if bufferLen + 1 == response.length:
                        break
                else:
                    tryAgain = input('[Error] Attempt failed. Try again? y/n ')

                    if tryAgain.lower() not in ('y', 'yes'):
                        return cls()
                        
                    thread.rx.clear()


        Package(type_='success').submit(thread=thread, timeout=timeout)

        return cls.decode(buffer)


    def submit (self, thread:Thread, timeout:int=-1):
        while True:
            with alive_bar(len(self), title='Sending') as bar:
                for package in self.encode():
                    package.submit(thread, timeout=timeout)
                    bar()

            success, done = Package.getSuccessDone(
                thread=thread,
                message=f'Failed do submit {self.type} stream.',
                timeout=timeout
            )

            if success and done:
                break
            else:
                thread.tx.clear()
                continue
