from lib.header import Header
from lib.thread import Thread
import time


class Package:
    PAYLOAD_SIZE = 114
    EOP = b'\xAA\xBB\xCC\xDD'


    def __init__ (self, type_:str='data', length:int=None, index:int=None, data:bytes=b''):
        self.type = type_
        self.length = length
        self.index = index
        self.data = data


    def encode (self):
        package = bytearray()
        header = Header(
            type_=self.type,
            index=self.index,
            length=self.length,
            size=len(self.data)
        )

        package.extend(header.encode())
        package.extend(self.data[0:self.PAYLOAD_SIZE])
        package.extend(self.EOP)

        return bytes(package)


    @classmethod
    def request (cls, thread:Thread, type_:str=None, index:int=None, length:int=None, size:int=None, timeout:int=20):
        header = Header.request(thread=thread, type_=type_, length=length, index=index, size=size, timeout=timeout/3)
        data, len_data = thread.receive(size=header.size, timeout=timeout/3)
        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout/3)

        if header.type == 'timeout' or len_data == 0 or len_eop == 0:
            package = TimeOut()

            package.submit(read=thread, timeout=timeout/3)

            return package

        elif (type_ and header.type != type_ or
            index and header.index != index or
            length and header.length != length or
            size and header.size != size and len_data == size or
            eop != cls.EOP
        ):
            error = Error(index=index)

            error.submit(thread=thread, timeout=timeout)

            return error

        elif header.type == 'data':
            Success(index=index).submit(thread=thread, timeout=timeout)

        return cls(
            type_=header.type,
            index=header.index,
            length=header.length,
            data=data
        )


    def submit (self, thread:Thread, timeout:int=-1):
        submit_success = True

        while True:
            thread.transmit(self.encode())

            if self.type == 'data':
                success, done = self.getSuccessDone(
                    thread=thread,
                    index=self.index,
                    timeout=timeout
                )

                if done:
                    submit_success = success
                    break
            else:
                break

        return submit_success


    @classmethod
    def getSuccessDone (cls, thread:Thread, index:int=1, timeout:int=None):
        response = cls.request(thread, type_='success', index=index, timeout=timeout)
        success = False
        done = False

        if response.type == 'error':
            done = True
        elif response.type == 'success':
            success = True
            done = True
        else:
            done = True

        return success, done


class Request (Package):
    def __init__ (self, target:int=0, length:int=None):
        super().__init__(type_='request', length=length, index=target)
        self.target = target


class Response (Package):
    def __init__ (self):
        super().__init__(type_='response')


class Data (Package):
    def __init__ (self, length:int=1, index:int=1, data:bytes=b''):
        super().__init__(type_='data', length=length, index=index, data=data)


class Success (Package):
    def __init__ (self, index:int=None):
        super().__init__(type_='success', index=index)


class TimeOut (Package):
    def __init__ (self):
        super().__init__(type_='timeout')


class Error (Package):
    def __init__ (self, index:int=None):
        super().__init__(type_='error', index=index)
