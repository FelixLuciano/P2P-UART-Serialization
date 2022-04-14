from lib.thread import Thread
import lib.header as header


class Package:
    PAYLOAD_SIZE = 114
    EOP = b'\xAA\xBB\xCC\xDD'
    _types = []


    def __init__ (self, length:int=1, index:int=1):
        self.length = length
        self.index = index


    @classmethod
    def register_type (cls, instance):
        cls._types.append(instance)


    def submit (self, thread:Thread):
        thread.transmit(self.encode())



class Request (Package):
    def __init__ (self, target:int=None, length:int=1):
        super().__init__(length=length)
        self.target = target


    def encode (self):
        package = bytearray()
        header_ = header.Request(
            target = self.target,
            length = self.length
        )

        package.extend(header_.encode())
        package.extend(self.EOP)

        return bytes(package)


    @classmethod
    def request (cls, thread:Thread, timeout:int=-1, *args, **kwargs):
        header_ = header.Request.request(thread=thread,timeout=timeout, *args, **kwargs)

        if type(header_) == Error:
            return Error(package_id=header_.package_id)
        elif type(header_) == Timeout:
            return Timeout()

        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout)

        if eop != cls.EOP:
            return Error()
        elif len_eop == 0:
            return Timeout(package_id=header_.package_id)

        return cls(
            target = header_.target,
            length = header_.length
        )



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
    def request (cls, thread:Thread, timeout:int=-1, *args, **kwargs):
        header_ = header.Response.request(thread=thread,timeout=timeout, *args, **kwargs)

        if type(header_) == Error:
            return Error(package_id=header_.package_id)
        elif type(header_) == Timeout:
            return Timeout()

        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout)

        if eop != cls.EOP:
            return Error(package_id=header_.package_id)
        elif len_eop == 0:
            return Timeout()

        return cls()



class Data (Package):
    def __init__ (self, length:int=1, index:int=1, data:bytes=b''):
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
            super().submit(thread=thread)

            response = Success(package_id=self.index).request(thread=thread, timeout=timeout)

            if type(response) == Error:
                response.submit(thread=thread)
            elif type(response) == Timeout:
                response.submit(thread=thread)
                break
            elif type(response) == Success:
                submit_success = True

        return submit_success


    @classmethod
    def request (cls, thread:Thread, timeout:int=-1, *args, **kwargs):
        header_ = header.Data.request(thread=thread,timeout=timeout, *args, **kwargs)

        if type(header_) == Error:
            error = Error(package_id = header_.package_id)

            error.submit(thread=thread, timeout=timeout)

            return error
        elif type(header_) == Timeout:
            return Timeout()

        data, len_data = thread.receive(size=header_.size, timeout=timeout)

        if len_data < header_.size:
            error =  Error(package_id=header_.index)

            error.submit(thread=thread, timeout=timeout)

            return error
        if len_data == 0:
            return Timeout()

        eop, len_eop = thread.receive(size=len(cls.EOP), timeout=timeout)

        if eop != cls.EOP:
            error = Error(package_id=header_.index)

            error.submit(thread=thread, timeout=timeout)

            return error
        elif len_eop == 0:
            return Timeout()

        Success(package_id=header_.index).submit(thread=thread)

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
    def request (cls, thread:Thread, timeout:int=-1, *args, **kwargs):
        header_ = header.Success.request(thread=thread,timeout=timeout, *args, **kwargs)

        if type(header_) == Error:
            return Error()
        elif type(header_) == Timeout:
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



Package.register_type(Request)
Package.register_type(Response)
Package.register_type(Data)
Package.register_type(Success)
Package.register_type(Timeout)
Package.register_type(Error)
