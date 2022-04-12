from lib.header import Header
from lib.thread import Thread
import time


class Package:
    PAYLOAD_SIZE = 114
    EOP = b'\xAA\xBB\xCC\xDD'


    def __init__ (self, type_:str='data', length:int=1, index:int=1, data:bytes=b''):
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
    def request (cls, thread:Thread, type_:str=None, index:int=None, length:int=None, size:int=None, timeout:int=None):
        header = Header.request(thread, timeout=timeout/3)
        data, _ = thread.receive(size=header.size, timeout=timeout/3)
        eop, _ = thread.receive(size=len(cls.EOP), timeout=timeout/3)

        if (type_ and header.type != type_ or
            index and header.index != index or
            length and header.length != length or
            size and header.size != size or
            eop != cls.EOP
        ):
            return Error(index=index)

        if header.type != 'success':
            Success(index=index).submit(thread=thread, timeout=timeout)

        types = {
            'request': Request,
            'response': Response,
            'data': Data,
            'success': Success,
            'timeout': TimeOut,
            'error': Error
        }

        return types.get(header.type, Data)(
            type_=header.type,
            index=header.index,
            length=header.length,
            data=data,
            id = header.id
        )


    def submit (self, thread:Thread, timeout:int=-1):
        while True:
            thread.transmit(self.encode())
            if self.type != 'success':
                success, done = self.getSuccessDone(
                    thread=thread,
                    index=self.index,
                    message=f'Failed do submit {self.type} at {self.index} of {self.length}.',
                    timeout=timeout
                )

                if success and done:
                    break
                if not success and done:
                    exit()
            else:
                break


    @classmethod
    def getSuccessDone (cls, thread:Thread, index:int=1, message:str='Attempt failed.', timeout:int=None):
        response = cls.request(thread, type_='success', index=index, timeout=timeout)

        if  response.type == 'error':
            print('[Error]', message, end=' ')

            tryAgain = input('Try again? y/n ')

            if tryAgain.lower() not in ('y', 'yes'):
                return False, True
            else:
                return False, False
        elif response.type == 'success':
            return True, True
        else:
            return False, True


class Request (Package):
    def __init__ (self, target:int=None, length:int=0):
        super().__init__(type_='request', length=length, index=target)
        self.target = target


class Response (Package):
    def __init__ (self):
        super().__init__(type_='response')


class Data (Package):
    def __init__ (self, length:int=1, index:int=1, data:bytes=b''):
        super().__init__(type_='data', length=length, index=index, data=data)


class Success (Package):
    def __init__ (self, package_id:int=None):
        super().__init__(type_='success', index=package_id)
        
        self.package_id = package_id


class TimeOut (Package):
    def __init__ (self):
        super().__init__(type_='timeout')


class Error (Package):
    def __init__ (self, package_id:int=None):
        super().__init__(type_='error', index=package_id)
        
        self.package_id = package_id
