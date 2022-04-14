import math

from alive_progress import alive_bar

from lib.thread import Thread
from lib.header import Header
from lib.package import Package, Request, Response, Data, Timeout


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

            yield Data(length=length, index=index+1, data=payload)


    @classmethod
    def decode (cls, stream:list):
        data = b''.join([package.data for package in stream])

        return cls(data=data)


    @classmethod
    def request (cls, thread:Thread, target:int=0, timeout:int=-1):
        buffer = []
        count = 1

        request = Request(target=target).request(thread=thread, timeout=timeout)

        Response().submit(thread=thread)

        with alive_bar(total=request.length, title='Receiving') as bar:
            while True:
                response = Data(length=request.length, index=count).request(thread=thread, timeout=timeout)

                if type(response) == Timeout:
                    return None
                
                buffer.append(response)
                bar()

                if response.index < request.length:
                    count += 1
                else:
                    break

        return cls.decode(buffer)


    def submit (self, thread:Thread, target:int=0, timeout:int=-1):
        length = len(self)

        Request(target=target, length=length).submit(thread=thread)

        response = Response().request(thread=thread, timeout=timeout)

        if type(response) == Timeout:
            return False
        
        with alive_bar(total=length, title='Submiting') as bar:
            for package in self.encode():
                success = package.submit(thread=thread, timeout=timeout)
                bar()

                if not success:
                    return False

        return True
