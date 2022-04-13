import time

from lib.thread import Thread
import lib.header as header


class Package:
    PAYLOAD_SIZE = 114
    EOP = b'\xAA\xBB\xCC\xDD'
    _types = {}


    def __init__ (self, length:int=1, index:int=1):
        self.length = length
        self.index = index


    @classmethod
    def register_type (cls, name:str, instance):
        cls._types[name] = instance


    def submit (self, thread:Thread):
        thread.transmit(self.encode())



class Request (Package):
    type = 'request'


    def __init__ (self, target:int=None):
        super().__init__()
        self.target = target


    def encode (self):
        package = bytearray()
        header_ = header.Request(
            target = self.target
        )

        package.extend(header_.encode())
        package.extend(self.EOP)

        return bytes(package)


    @classmethod
    def request (cls, thread:Thread, timeout:int=None, *args, **kwargs):
        header_ = header.Request.request(thread=thread,timeout=timeout, *args, **kwargs)

        if header_.type == 'error':
            return Error()
        elif header_.type == 'timeout':
            return Timeout()

        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout)

        if eop != cls.EOP:
            return Error()
        elif len_eop == 0:
            return Timeout()

        return cls(target=header_.target)



class Response (Package):
    def __init__ (self):
        super().__init__()


    def encode (self):
        package = bytearray()
        header_ = header.Response()

        package.extend(header_.encode())
        package.extend(self.EOP)

        return bytes(package)


    @classmethod
    def request (cls, thread:Thread, timeout:int=None, *args, **kwargs):
        header_ = header.Response.request(thread=thread,timeout=timeout, *args, **kwargs)

        if header_.type == 'error':
            return Error(package_id=header_.package_id)
        elif header_.type == 'timeout':
            return Timeout()

        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout)

        if eop != cls.EOP:
            return Error(package_id=header_.header_)
        elif len_eop == 0:
            return Timeout()

        return cls()



class Data (Package):
    def __init__ (self, length:int=None, index:int=None, data:bytes=b''):
        super().__init__(length=length, index=index)
        self.data = data


    def __len__ (self):
        return len(self.data)


    def encode (self):
        package = bytearray()
        header_ = header.Data(
            length=self.length,
            index=self.index,
            size=len(self),
        )

        package.extend(header_.encode())
        package.extend(self.data)
        package.extend(self.EOP)

        return bytes(package)


    def submit (self, thread:Thread, timeout:int=-1):
        submit_success = False

        while not submit_success:
            thread.transmit(self.encode())

            response = Success(package_id=self.index).request(thread=thread, timeout=timeout)

            if response.type == 'error':
                response.submit(thread=thread, timeout=timeout)
            elif response.type == 'timeout':
                response.submit(thread=thread, timeout=timeout)
                break
            elif response.type == 'success':
                submit_success = True

        return submit_success


    @classmethod
    def request (cls, thread:Thread, timeout:int=None, *args, **kwargs):
        header_ = header.Data.request(thread=thread,timeout=timeout, *args, **kwargs)

        if header_.type == 'error':
            return Error(package_id = header_.package_id)
        elif header_.type == 'timeout':
            return Timeout()

        data, len_data = thread.receive(size=header_.size, timeout=timeout)

        if len_data < header_.size:
            return Error(package_id=header_.index)
        if len_data == 0:
            return Timeout()

        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout)

        if eop != cls.EOP:
            return Error(package_id=header_.index)
        elif len_eop == 0:
            return Timeout()

        return cls(
            length = header_.length,
            index = header_.index,
            data = data
        )



class Success (Package):
    def __init__ (self, package_id:int=None):
        super().__init__()
        self.package_id = package_id


    def encode (self):
        package = bytearray()
        header_ = header.Success(
            package_id = self.package_id
        )

        package.extend(header_.encode())
        package.extend(self.EOP)

        return bytes(package)


    @classmethod
    def request (cls, thread:Thread, timeout:int=None, *args, **kwargs):
        header_ = header.Success.request(thread=thread,timeout=timeout, *args, **kwargs)

        if header_.type == 'error':
            return Error()
        elif header_.type == 'timeout':
            return Timeout()

        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout)

        if eop != cls.EOP:
            return Error()
        elif len_eop == 0:
            return Timeout()

        return cls(package_id=header_.package_id)



class Timeout (Package):
    def __init__ (self):
        super().__init__()


    def encode (self):
        package = bytearray()
        header_ = header.Timeout()

        package.extend(header_.encode())
        package.extend(self.EOP)

        return bytes(package)



class Error (Package):
    def __init__ (self, package_id:int=None):
        super().__init__()
        self.package_id = package_id


    def encode (self):
        package = bytearray()
        header_ = header.Error(
            package_id = self.package_id
        )

        package.extend(header_.encode())
        package.extend(self.EOP)

        return bytes(package)



Package.register_type('request', Request)
Package.register_type('response', Response)
Package.register_type('data', Data)
Package.register_type('success', Success)
Package.register_type('timeout', Timeout)
Package.register_type('error', Error)

