import math

from alive_progress import alive_bar

from lib.thread import Thread
from lib.header import Header
from lib.package import Package, Request, Data


class Stream:
    PACKAGE_SIZE = 128
    PAYLOAD_SIZE = PACKAGE_SIZE - Header.SIZE - len(Package.EOP)


    def __init__ (self, data:bytes=b''):
        self.data = data


    def __len__ (self):
        return math.ceil(len(self.data) / self.PAYLOAD_SIZE)


    def encode(self):
        for index, step in enumerate(range(0, len(self.data), self.PAYLOAD_SIZE)):
            payload = self.data[step:step+self.PAYLOAD_SIZE]

            yield Data(length=len(self), index=index, data=payload)


    @classmethod
    def decode (cls, stream:list):
        data = b''.join([package.data for package in stream])

        return cls(data=data)


    @classmethod
    def request (cls, thread:Thread, target:int=0, timeout:int=-1):
        buffer = []
        count = 1

        request = Request(target=target).request(thread=thread, timeout=timeout)

        with alive_bar(title='Receiving', manual=True) as bar:
            while True:
                response = Package.request(thread, type_='data', index=count, timeout=timeout)

                if response.type == 'data':
                    buffer.append(response)
                    bar(count / request.length)

                    if count < request.length:
                        count == 1
                    else:
                        break
                elif response.type == 'timeout':
                    return None
                else:
                    thread.rx.clear()

        return cls.decode(buffer)


    def submit (self, thread:Thread, target:int=0, timeout:int=-1):
        # while True:
        #     with alive_bar(len(self), title='Sending') as bar:
        #         for package in self.encode():
        #             package.submit(thread, timeout=timeout)
        #             bar()

        #     success, done = Package.getSuccessDone(
        #         thread=thread,
        #         message=f'Failed do submit {self.type} stream.',
        #         timeout=timeout
        #     )

        #     if success and done:
        #         break
        #     else:
        #         thread.tx.clear()
        #         continue
        return None
