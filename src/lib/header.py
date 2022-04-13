from lib.thread import Thread


class Header:
    SIZE = 10
    _types = {}


    def __init__ (self, length:int=1, index:int=1, size:int=0):
        self.length = length
        self.index = index
        self.size = size


    @classmethod
    def register_type (cls, name:str, instance):
        cls._types[name] = instance


    @classmethod
    def get_type (cls, type_bytes:bytes):
        type_value = int.from_bytes(type_bytes, 'big')

        for name, instance in cls._types.items():
            if type_value == instance.type_byte:
                return name


    def encode (self):
        header = bytearray()

        # Byte h0 - Package type
        header.extend(self.type_byte.to_bytes(1, 'big'))

        # Byte h1 - NC
        header.extend((0).to_bytes(1, 'big'))

        # Byte h2 - NC
        header.extend((0).to_bytes(1, 'big'))

        # Byte h3 - Stream length
        header.extend(self.length.to_bytes(1, 'big'))

        # Byte h4 - Package index
        header.extend(self.index.to_bytes(1, 'big'))

        # Byte h5, h6, h7 - Reserved to type
        header.extend((0).to_bytes(1, 'big'))
        header.extend((0).to_bytes(1, 'big'))
        header.extend((0).to_bytes(1, 'big'))

        # Byte h8 - CRC
        header.extend((0).to_bytes(1, 'big'))

        # Byte h9 - CRC
        header.extend((0).to_bytes(1, 'big'))

        return header


    @classmethod
    def decode (cls, data:bytes, *args, **kwargs):
        type_ = cls.get_type(data[0:1])
        instance = cls._types[type_]

        return instance.decode(data, *args, **kwargs)


    @classmethod
    def request (cls, thread:Thread, timeout:int=None, *args, **kwargs):
        data, len_data = thread.receive(cls.SIZE, timeout=timeout)

        if len_data == 0:
            return Timeout()

        return cls.decode(data, *args, **kwargs)



class Request (Header):
    type = 'request'
    type_byte = 0x01


    def __init__ (self, target:int=0):
        super().__init__()
        self.target = target

    @classmethod
    def decode (cls, data:bytes):
        return cls(
          target = int.from_bytes(data[5:6], 'big')
        )

    def encode (self):
        data = super().encode()

        data[5:6] = self.target.to_bytes(1, 'big')

        return data


class Response (Header):
    type = 'response'
    type_byte = 0x02


    def __init__ (self):
        super().__init__()


    @classmethod
    def decode (cls, data:bytes):
        return cls()


    def encode (self):
        return super().encode()



class Data (Header):
    type = 'data'
    type_byte = 0x03


    def __init__ (self, length:int=1, index:int=1, size:int=0):
        super().__init__(length=length, index=index, size=size)


    @classmethod
    def decode (cls, data:bytes, length:int=None, index:int=None, size:int=None):
        header = cls(
          length = int.from_bytes(data[3:4], 'big'),
          index = int.from_bytes(data[4:5], 'big'),
          size = int.from_bytes(data[5:6], 'big')
        )

        if (
          length and header.length != length or
          index and header.index != index or
          size and header.size != size
        ):
          return Error(package_id=index)

        return header


    def encode (self):
        data = super().encode()

        data[5:6] = self.size.to_bytes(1, 'big')

        return data



class Success (Header):
    type = 'success'
    type_byte = 0x04


    def __init__ (self, package_id:int=0):
        super().__init__()
        self.package_id = package_id


    @classmethod
    def decode (cls, data:bytes, package_id:int=0):
        header = cls(
          package_id=int.from_bytes(data[7:8], 'big')
        )

        if package_id and header.package_id != package_id:
          return Error(package_id=package_id)

        return header


    def encode (self):
        data = super().encode()

        data[7:8] = self.package_id.to_bytes(1, 'big')

        return data



class Timeout (Header):
    type = 'timeout'
    type_byte = 0x05


    def __init__ (self):
        super().__init__()


    @classmethod
    def decode (cls, data:bytes):
        return cls()


    def encode (self):
        return super().encode()



class Error (Header):
    type = 'error'
    type_byte = 0x06


    def __init__ (self, package_id:int=0):
        super().__init__()
        self.package_id = package_id


    @classmethod
    def decode (cls, data:bytes, package_id:int=None):
        header = cls(
          package_id=int.from_bytes(data[6:7], 'big')
        )

        if package_id and header.package_id != package_id:
          return Error(package_id=package_id)

        return header


    def encode (self):
        data = super().encode()

        data[6:7] = self.package_id.to_bytes(1, 'big')

        return data



Header.register_type('request', Request)
Header.register_type('response', Response)
Header.register_type('data', Data)
Header.register_type('success', Success)
Header.register_type('timeout', Timeout)
Header.register_type('error', Error)
