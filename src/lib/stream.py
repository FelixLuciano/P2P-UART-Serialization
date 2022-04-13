import math

from alive_progress import alive_bar

from lib.thread import Thread
from lib.header import Header
from lib.package import Package, Request, Response


class Data_stream:
    PACKAGE_SIZE = 128
    PAYLOAD_SIZE = PACKAGE_SIZE - Header.SIZE - len(Package.EOP)


    def __init__ (self, data:bytes=b''):
        self.data = data


    def __len__ (self):
        return math.ceil(len(self.data) / self.PAYLOAD_SIZE)


    def encode(self):
        length=len(self)

        for index, step in enumerate(range(0, len(self.data), self.PAYLOAD_SIZE)):
            payload = self.data[step:step+self.PAYLOAD_SIZE]

            yield Data(length=length, index=index, data=payload)


    @classmethod
    def decode (cls, stream:list):
        data = b''.join([package.data for package in stream])

        return cls(data=data)


    @classmethod
    def request (cls, thread:Thread, target:int=0, timeout:int=None):
        buffer = []
        count = 1

        request = Request(target=target).request(thread=thread, timeout=timeout)

        Response().submit(thread=thread, timeout=timeout)

        with alive_bar(title='Receiving', manual=True) as bar:
            while True:
                response = Data(length=request.length, index=count).request(thread=thread, timeout=timeout)

                if response.type == 'timeout':
                    return None
                
                buffer.append(response.data)

                if response.index < request.length:
                    bar(count / request.length)
                    count += 1
                else:
                    break

        return cls.decode(buffer)


    def submit (self, thread:Thread, target:int=0, timeout:int=None):
        Request(target=target).submit(thread=thread, timeout=timeout)

        response = Response().request(thread=thread, timeout=timeout)

        if response.type == 'timeout':
            return False
        
        with alive_bar(title='Submiting', manual=True) as bar:
            for count, package in enumerate(self.encode()):
                package.submit(thread=thread, timeout=timeout)
                bar(count / len(self))

        return True
